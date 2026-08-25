#!/usr/bin/env python3
"""Summarize the complete historical-archive old/custom tile scan."""

from __future__ import annotations

import collections
import json
import os
import tempfile
import urllib.parse
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "map-inventory" / "historical-archive-candidates.jsonl"
SUMMARY = ROOT / "map-inventory" / "historical-archive-scan.json"
OUTPUT = ROOT / "historical-map-features.md"
KNOWN_TELE = {10, 14, 15, 26, 27, 29, 30, 31, 63}


def display_name(uri: str) -> str:
    return urllib.parse.unquote(uri.rsplit("/", 1)[-1])


def main() -> None:
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    strong: list[tuple[str, str, int, tuple[int, ...]]] = []
    unknown_tele: list[tuple[str, str, tuple[int, ...]]] = []
    entity_distribution: collections.Counter[int] = collections.Counter()
    tele_distribution: collections.Counter[int] = collections.Counter()
    combinations: collections.Counter[tuple[int, ...]] = collections.Counter()
    errors: list[tuple[str, str]] = []

    for line in INVENTORY.read_text(encoding="utf-8").splitlines():
        record = json.loads(line)
        if "error" in record:
            errors.append((record["path"], record["error"]))
            continue
        entity_ids: set[int] = set()
        tele_ids: set[int] = set()
        for layer in record["layers"]:
            for name in ("game", "front"):
                entity_ids.update(map(int, layer.get(name, {})))
            tele_ids.update(map(int, layer.get("tele", {})))
        entity_distribution.update(entity_ids.intersection(range(128, 192)))
        tele_distribution.update(tele_ids)
        old = tuple(sorted(entity_ids.intersection(range(176, 190))))
        if old:
            combinations[old] += 1
            strong.append((record["path"], record["sha256"], record["size"], old))
        extra_tele = tuple(sorted(tele_ids - KNOWN_TELE))
        if extra_tele:
            unknown_tele.append((record["path"], record["sha256"], extra_tele))

    lines = [
        "# Complete historical map feature scan",
        "",
        "This report covers one byte-verified representative of every content hash in the immutable mirror plus all four authoritative delta maps. The scanner records raw entity bytes; it does not assign a historical mod solely from a tile number.",
        "",
        "## Scan identity",
        "",
        f"- Archive SHA-256: `{summary['archive_sha256']}`",
        f"- Archive size: `{summary['archive_size']}` bytes",
        f"- Archive members: `{summary['archive_members']}`",
        f"- Distinct archive hashes: `{summary['archive_unique_hashes']}`",
        f"- Authoritative delta maps: `{summary['delta_maps']}`",
        f"- Total distinct contents scanned: `{summary['scanned_unique_hashes']}`",
        f"- Broad custom/collision candidates retained: `{summary['candidate_records']}`",
        f"- Parse failures retained: `{summary['parse_failures']}`",
        f"- Complete canonical-result digest: `{summary['complete_scan_sha256']}`",
        f"- Peak transient extraction: `{summary['peak_temporary_batch_bytes']}` bytes",
        "",
        "The authoritative Heinrich set is 47,959 hashes. The mirror also contains additional map objects, which are scanned for discovery but do not become authoritative merely by being present.",
        "",
        "## Tile-family findings",
        "",
        f"- Maps with at least one raw game/front ID 176–189: `{len(strong)}`",
        f"- Maps with a non-current tele-layer type byte: `{len(unknown_tele)}`",
        "- Canonical XXLDDRace maps use 176–185 and 189–191; TBlock deliberately assigns different meanings to 178–189; modern DDNet uses 190–191 as overlay signs.",
        "- The full 128–191 candidate records remain in `map-inventory/historical-archive-candidates.jsonl` so later family classifiers can be rerun without expanding the archive.",
        "",
        "## Raw ID prevalence",
        "",
    ]
    lines.extend(f"- `{tile}`: {entity_distribution[tile]} maps" for tile in sorted(entity_distribution))
    lines.extend(["", "## Most common 176–189 combinations", ""])
    for combination, count in combinations.most_common(100):
        lines.append(f"- `{','.join(map(str, combination))}`: {count} maps")
    lines.extend(["", "## Maps carrying IDs 176–189", ""])
    for uri, digest, size, identifiers in sorted(strong, key=lambda item: (display_name(item[0]).casefold(), item[1])):
        lines.append(f"- `{display_name(uri)}` — `{digest}`, {size} bytes, IDs `{','.join(map(str, identifiers))}`, source `{uri}`")
    lines.extend(["", "## Non-current tele-layer type candidates", ""])
    for uri, digest, identifiers in sorted(unknown_tele, key=lambda item: (display_name(item[0]).casefold(), item[1])):
        lines.append(f"- `{display_name(uri)}` — `{digest}`, types `{','.join(map(str, identifiers))}`, source `{uri}`")
    lines.extend(["", "## Parse failures", ""])
    for uri, error in sorted(errors):
        lines.append(f"- `{uri}` — {error}")
    lines.append("")

    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{OUTPUT.name}.", dir=OUTPUT.parent, text=True)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as output:
            output.write("\n".join(lines))
            output.flush()
            os.fsync(output.fileno())
        os.chmod(temporary_name, 0o664)
        os.replace(temporary_name, OUTPUT)
    finally:
        if os.path.exists(temporary_name):
            os.unlink(temporary_name)


if __name__ == "__main__":
    main()
