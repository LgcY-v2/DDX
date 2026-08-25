#!/usr/bin/env python3
"""Create deterministic raw feature inventories for every archived candidate."""

from __future__ import annotations

import collections
import hashlib
import io
import json
import os
import re
import subprocess
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
REPOSITORIES = ROOT / "repositories" / "github"
DDX_ROOT = ROOT.parents[1]
TEXT_SUFFIXES = {".c", ".cc", ".cpp", ".h", ".hpp", ".py", ".sh", ".cfg", ".md", ".txt"}
SKIP_PARTS = {".git", "build", "build64", "cmake-build-debug", "cmake-build-release", "vendor", "node_modules"}
REGISTER = re.compile(r'\bRegister\s*\(\s*"([a-zA-Z0-9_+.-]+)"\s*,\s*"([^"]*)"[^\n]*?"([^"]*)"\s*\)')
CONFIG_CALL = re.compile(r'MACRO_CONFIG_(?:INT|STR|COL|FLOAT)\s*\((.*)\)\s*$')
TILE = re.compile(r'\b(?:TILE|ENTITY)_[A-Z][A-Z0-9_]*\b')


CURATED = {
    "canonical": [
        "Game/front tile 176 toggles cycling rainbow body/feet colors.",
        "Tile 177 toggles XXL rapid fire for ordinary weapons by changing the character reload multiplier from 1000 to 10000; optional silent-XXL suppresses repeated fire sounds.",
        "Tiles 178 and 179 are access gates for the old numeric admin and member-list models. These authentication implementations must not be copied into DDX.",
        "Tile 180 toggles super: unfreezes the tee, moves it to the super team, and marks the run cheated; crossing again restores the previous team.",
        "Tile 181 toggles the heavy-hammer mode; tile 182 toggles network invisibility; tile 183 toggles the blood death-particle trail.",
        "Tile 184 removes all XXL extras; tile 185 removes ninja.",
        "Tiles 189, 190, and 191 set the jump count to two, increment it, and decrement it. Modern DDNet reuses 190 and 191 as entity-overlay signs.",
        "Commands expose the same rainbow, bloody, XXL, invisibility, heavy-hammer, super, fly, jump-count, weapon, and moderation states without requiring a tile.",
        "The server has a separate member file/login model and old helper/subadmin/mod/admin ranks. DDX has a different owner/admin contract, so only capability semantics are candidates.",
        "The client/editor recognizes and renders the XXL entities; server-only support would leave old maps hard to inspect and edit.",
    ],
    "ftk": [
        "Includes the canonical XXL tile and command behavior listed above.",
        "Adds per-character tune tiles across raw IDs 0x80–0xAF for air-jump impulse, laser reach/bounces, hook length, ground/air control speed, ground jump impulse, player collision, gravity, friction, and player hooking.",
        "IDs 0xBA and 0xBB enable and disable the character rescue override.",
        "The extra-tile range overlaps canonical XXL IDs and multiple modern DDNet IDs; it cannot be enabled globally without a proven map-family discriminator.",
        "Adds `tune_player`, fake-chat, private-message, silent-rename, solo/swap/text, rescue, and other server/chat controls found in the raw command inventory.",
        "Contains client-side aimline, aimbot prediction/smoothing, delayed-input time-machine, and related controls. These are research artifacts, not automatically suitable DDX server features.",
    ],
    "tblock": [
        "Reassigns the XXL range: 176 rainbow, 177 rapid fire, 178 member gate, 179 super, 180 heavy hammer, 181 invisibility, 182 bloody, 183–186 named clan gates, 187 remove extras, 188 a skin-gated mafia room, and 189 invisibility-off.",
        "Adds raw IDs 164 (VeNuM clan gate), 166 (moderator gate), 167 (administrator gate), and 168 (global gun/explosion sound trigger).",
        "Clan gates compare client-supplied clan strings and kill non-members; the mafia gate compares the skin. These are historical map semantics, not secure authorization mechanisms.",
        "Its member gate uses a local account/member login system distinct from both canonical XXLDDRace and DDX.",
        "Because IDs 178–189 conflict with canonical XXLDDRace, TBlock maps require explicit family selection or reliable map fingerprints.",
    ],
    "ddnetpp": [
        "Retains named XXL-style rainbow and bloody tiles inside a much larger DDNet++ minigame/blocker/city codebase.",
        "Adds accounts, money/experience, shops, minigames, survival/blocking systems, dummies/bots, spawn/weapons utilities, and extensive administration controls; see the raw source-only command/config/tile inventories below.",
        "Its modern code and persisted account model are independent of historical XXL map compatibility and must remain opt-in.",
    ],
    "fddrace": [
        "Carries forward XXL-style rainbow/bloody and related blocker/city extras on a later DDNet base.",
        "Some later variants add a combined teleport input/output tile family. `fokkonaut/F-DDrace` and `xuilan42/f-ddracePlus` assign normal/evil variants to raw tele types 93/94, while `nameless-me/F-DDrace` and `uvi-q/fddr` assign them to 95/94; compatibility therefore requires an explicit source-family decision.",
        "Adds account/currency/progression, cosmetic and weapon effects, minigame/blocker utilities, and administration controls identified below.",
        "The persistence and social-game systems are not required merely to run an old XXL map and must remain separately selectable.",
    ],
    "blocker": [
        "Uses XXL-style rainbow/bloody tile or character state inside a blocker-oriented derivative.",
        "Adds blocker, punishment, account/database, bot/dummy, cosmetic, and administration behavior identified by the raw inventories below.",
        "Only source-proven map semantics are compatibility candidates; server-community policy and persistence are separate product choices.",
    ],
    "adjacent": [
        "This is an adjacent DDRace-derived source or map corpus, retained because it shares XXL source signatures, history, maps, or later implementations of XXL-style features.",
        "No family-wide semantic claim is inferred from the repository name. The literal source differences below are the review surface.",
    ],
    "deployment": [
        "This candidate packages, indexes, or deploys another server rather than defining a distinct gameplay implementation.",
        "Its useful differences are build/runtime assumptions and bundled map or configuration provenance, listed below.",
    ],
}


def text_files(root: Path):
    for directory, names, files in os.walk(root):
        names[:] = sorted(name for name in names if name not in SKIP_PARTS)
        for filename in sorted(files):
            path = Path(directory) / filename
            if filename == "xfeatures.md" or path.suffix.lower() not in TEXT_SUFFIXES:
                continue
            try:
                yield path, path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue


def config_entry(line: str) -> tuple[str, str] | None:
    """Read both old one-name and modern symbol/script-name config macros."""
    match = CONFIG_CALL.search(line)
    if not match:
        return None
    fields = match.group(1).split(",", 2)
    if len(fields) < 2:
        return None
    first = fields[0].strip()
    second = fields[1].strip()
    name = second if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", second) else first
    descriptions = re.findall(r'"([^"]*)"', match.group(1))
    return name, descriptions[-1] if descriptions else ""


def inventory(root: Path) -> dict[str, dict[str, list[str]]]:
    commands: dict[str, list[str]] = collections.defaultdict(list)
    configs: dict[str, list[str]] = collections.defaultdict(list)
    tiles: dict[str, list[str]] = collections.defaultdict(list)
    signatures: dict[str, list[str]] = collections.defaultdict(list)
    for path, content in text_files(root):
        relative = str(path.relative_to(root))
        for number, line in enumerate(content.splitlines(), 1):
            for match in REGISTER.finditer(line):
                commands[match.group(1)].append(f"{relative}:{number} | `{match.group(2)}` | {match.group(3)}")
            config = config_entry(line)
            if config is not None:
                configs[config[0]].append(f"{relative}:{number} | {config[1]}")
            for match in TILE.finditer(line):
                tiles[match.group(0)].append(f"{relative}:{number}")
            lowered = line.lower()
            for term in ("xxl", "rainbow", "bloody", "fastreload", "fast_reload", "invisible", "rescueoverride"):
                if term in lowered:
                    signatures[term].append(f"{relative}:{number}")
    return {"commands": commands, "configs": configs, "tiles": tiles, "signatures": signatures}


def inventory_ref(repo: Path, ref: str) -> dict[str, dict[str, list[str]]]:
    """Inventory text blobs at a Git ref without mutating the candidate checkout."""
    result: dict[str, dict[str, list[str]]] = {
        "commands": collections.defaultdict(list),
        "configs": collections.defaultdict(list),
        "tiles": collections.defaultdict(list),
        "signatures": collections.defaultdict(list),
    }
    archive = subprocess.check_output(["git", "-C", repo, "archive", "--format=tar", ref], stderr=subprocess.DEVNULL)
    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:") as stream:
        members = sorted((member for member in stream if member.isfile()), key=lambda item: item.name)
        blobs = []
        for member in members:
            path = Path(member.name)
            if path.name == "xfeatures.md" or path.suffix.lower() not in TEXT_SUFFIXES or any(part in SKIP_PARTS for part in path.parts):
                continue
            extracted = stream.extractfile(member)
            if extracted is not None:
                blobs.append((member.name, extracted.read().decode("utf-8", errors="replace")))
    for relative, content in blobs:
        for number, line in enumerate(content.splitlines(), 1):
            for match in REGISTER.finditer(line):
                result["commands"][match.group(1)].append(f"{relative}:{number}")
            config = config_entry(line)
            if config is not None:
                result["configs"][config[0]].append(f"{relative}:{number}")
            for match in TILE.finditer(line):
                result["tiles"][match.group(0)].append(f"{relative}:{number}")
            lowered = line.lower()
            for term in ("xxl", "rainbow", "bloody", "fastreload", "fast_reload", "invisible", "rescueoverride"):
                if term in lowered:
                    result["signatures"][term].append(f"{relative}:{number}")
    return result


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", repo, *args], text=True, stderr=subprocess.DEVNULL).strip()


def profile(name: str, data: dict[str, dict[str, list[str]]]) -> str:
    tiles = data["tiles"]
    lowered = name.lower()
    if "docker" in lowered or name in {"ItzGuuh/Teeworlds", "miguilimzero/teeworlds-mods"}:
        return "deployment"
    if "TILE_VCLAN" in tiles:
        return "tblock"
    if "TILE_EXTRA_START" in tiles:
        return "ftk"
    if name.startswith("DDNetPP/"):
        return "ddnetpp"
    if "f-ddrace" in lowered or name == "uvi-q/fddr":
        return "fddrace"
    if "block" in lowered or name in {"tw-blnet/blmod", "veljko-radovanovic/lonerstuff"}:
        return "blocker"
    if "TILE_RMEXTRAS" in tiles and "TILE_JUMPS_DEFAULT" in tiles:
        return "canonical"
    return "adjacent"


def map_records() -> list[dict[str, object]]:
    result = []
    path = ROOT / "map-inventory" / "repository-maps.jsonl"
    if path.exists():
        result.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines())
    return result


def section(lines: list[str], title: str, values: dict[str, list[str]], baseline: set[str]) -> None:
    missing = sorted(set(values) - baseline)
    lines.extend([f"## {title}", ""])
    if not missing:
        lines.extend(["No literal identifiers absent from the current DDX source were found.", ""])
        return
    for name in missing:
        evidence = sorted(set(values[name]))
        lines.append(f"- `{name}` — {'; '.join(evidence[:4])}" + (f"; and {len(evidence) - 4} more locations" if len(evidence) > 4 else ""))
    lines.append("")


def branch_section(lines: list[str], repo: Path, branches: list[str], head_data: dict[str, dict[str, list[str]]]) -> None:
    lines.extend(["## Fetched remote branch audit", ""])
    if not branches:
        lines.extend(["No fetched non-default remote branch exists.", ""])
        return
    head_commit = git(repo, "rev-parse", "HEAD")
    for branch in branches:
        commit = git(repo, "rev-parse", branch)
        tree = git(repo, "rev-parse", f"{branch}^{{tree}}")
        if commit == head_commit:
            lines.append(f"- `{branch}` — commit `{commit}`, tree `{tree}`; same commit as archived HEAD.")
            continue
        data = inventory_ref(repo, branch)
        deltas = []
        for category, label in (("commands", "commands"), ("configs", "configs"), ("tiles", "tiles")):
            unique = sorted(set(data[category]) - set(head_data[category]))
            if unique:
                deltas.append(f"{label}: " + ", ".join(f"`{item}`" for item in unique))
        signature_deltas = []
        for term in sorted(data["signatures"]):
            change = len(data["signatures"][term]) - len(head_data["signatures"].get(term, []))
            if change:
                signature_deltas.append(f"`{term}` {change:+d} lines")
        detail = "; ".join(deltas + signature_deltas) or "no new literal command/config/tile identifiers or XXL signature count changes"
        lines.append(f"- `{branch}` — commit `{commit}`, tree `{tree}`; {detail}.")
    lines.append("")


def write_report(repo: Path, name: str, data: dict[str, dict[str, list[str]]], ddx: dict[str, dict[str, list[str]]], maps: list[dict[str, object]]) -> None:
    head = git(repo, "rev-parse", "HEAD")
    tree = git(repo, "rev-parse", "HEAD^{tree}")
    branches = git(repo, "for-each-ref", "--format=%(refname:short)", "refs/remotes/origin").splitlines()
    branches = [branch for branch in branches if branch not in ("origin", "origin/HEAD")]
    repo_prefix = str(repo.relative_to(DDX_ROOT)) + "/"
    own_maps = [record for record in maps if str(record.get("path", "")).startswith(repo_prefix)]
    kind = profile(name, data)
    ddx_revision = git(DDX_ROOT, "rev-parse", "HEAD")
    patch_files = sorted((DDX_ROOT / "patches").glob("*.patch"))
    patch_identity = ", ".join(
        f"`{path.name}` `{hashlib.sha256(path.read_bytes()).hexdigest()}`" for path in patch_files
    )
    lines = [
        f"# {name} feature inventory",
        "",
        f"This is a source-derived research inventory against DDX at `{ddx_revision}`. Literal raw inventories deliberately over-include review candidates; they do not imply that unsafe authentication, cheats, persistence, or community policy should be ported.",
        "",
        f"Numbered DDX patch inputs: {patch_identity}.",
        "",
        "## Archived identity",
        "",
        f"- HEAD commit: `{head}`",
        f"- HEAD tree: `{tree}`",
        f"- Archived remote branches: `{', '.join(branches) or 'none'}`",
        f"- Full Git connectivity check: recorded as successful in `sources.tsv`.",
        "",
        "## Source-proven feature differences",
        "",
    ]
    lines.extend(f"- {item}" for item in CURATED[kind])
    lines.append("")
    branch_section(lines, repo, branches, data)
    section(lines, "Raw command identifiers absent from DDX", data["commands"], set(ddx["commands"]))
    section(lines, "Raw configuration identifiers absent from DDX", data["configs"], set(ddx["configs"]))
    section(lines, "Raw tile/entity symbols absent from DDX", data["tiles"], set(ddx["tiles"]))
    lines.extend(["## XXL source signatures", ""])
    if data["signatures"]:
        for term in sorted(data["signatures"]):
            evidence = sorted(set(data["signatures"][term]))
            lines.append(f"- `{term}`: {len(evidence)} source lines; first locations: {', '.join(evidence[:8])}")
    else:
        lines.append("No literal XXL/rainbow/bloody/fast-reload/invisibility/rescue-override signature was found in the scanned text files.")
    lines.extend(["", "## Bundled maps", ""])
    if own_maps:
        for record in sorted(own_maps, key=lambda item: str(item.get("path", ""))):
            if "error" in record:
                lines.append(f"- `{record['path']}` — parse error retained in central inventory: {record['error']}")
                continue
            ids: set[int] = set()
            for layer in record["layers"]:
                for layer_name in ("game", "front"):
                    ids.update(map(int, layer.get(layer_name, {})))
            old = sorted(ids.intersection(range(176, 192)))
            lines.append(f"- `{record['path']}` — `{record['sha256']}`, {record['size']} bytes, IDs 176–191: `{','.join(map(str, old)) or 'none'}`")
    else:
        lines.append("No `.map` file was found in this repository checkout.")
    lines.extend(
        [
            "",
            "## Compatibility cautions",
            "",
            "- Raw tile IDs are not globally unique across historical mods. Select semantics from a fingerprinted map family or explicit administrator setting; fail closed on ambiguity.",
            "- Do not import candidate credentials, account databases, trust-by-clan/skin, or old numeric authorization ranks.",
            "- Reimplement selected behavior on current DDNet/DDX primitives and validate it with deterministic map/character replay tests.",
            "",
        ]
    )
    destination = repo / "xfeatures.md"
    descriptor, temporary_name = tempfile.mkstemp(prefix=".xfeatures.", dir=repo, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            output.write("\n".join(lines))
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary_name, destination)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


def main() -> None:
    ddx = inventory(DDX_ROOT / "source" / "ddnet")
    patch_inventory = inventory(DDX_ROOT / "patches")
    for category in ddx:
        for key, values in patch_inventory[category].items():
            ddx[category][key].extend(values)
    maps = map_records()
    for owner in sorted(REPOSITORIES.iterdir()):
        for repo in sorted(path for path in owner.iterdir() if (path / ".git").is_dir()):
            name = f"{owner.name}/{repo.name}"
            # The canonical repository has a longer hand-audited report.
            if name == "AdVetter/XXLDDRace":
                continue
            write_report(repo, name, inventory(repo), ddx, maps)


if __name__ == "__main__":
    main()
