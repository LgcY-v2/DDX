#!/usr/bin/env python3
"""Generate the human-readable old-tile map corpus report."""

from __future__ import annotations

import collections
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
INVENTORY = ROOT / "map-inventory"
OUTPUT = ROOT / "map-compatibility.md"


def main() -> None:
    records: dict[str, dict[str, object]] = {}
    locations: dict[str, list[str]] = collections.defaultdict(list)
    errors: list[dict[str, str]] = []
    for inventory in sorted(INVENTORY.glob("*.jsonl")):
        if inventory.name == "historical-archive-candidates.jsonl":
            continue
        for line in inventory.read_text(encoding="utf-8").splitlines():
            record = json.loads(line)
            if "error" in record:
                errors.append({"inventory": inventory.name, **record})
                continue
            digest = record["sha256"]
            records.setdefault(digest, record)
            locations[digest].append(record["path"])

    candidates: list[tuple[str, list[int], list[int], dict[str, object]]] = []
    for digest, record in records.items():
        game_front: set[int] = set()
        tele: set[int] = set()
        for layer in record["layers"]:
            for kind in ("game", "front"):
                game_front.update(map(int, layer.get(kind, {})))
            tele.update(map(int, layer.get("tele", {})))
        strong = sorted(game_front.intersection(range(176, 190)))
        ambiguous = sorted(game_front.intersection((190, 191)))
        if strong or ambiguous:
            candidates.append((digest, strong, ambiguous, record))

    lines = [
        "# Historical map compatibility inventory",
        "",
        "Generated from raw Teeworlds datafile entity layers by `scan_maps.py`. Files are deduplicated by full SHA-256; all observed locations remain listed.",
        "",
        "IDs 176–185 are strong XXL-family indicators. IDs 186–188 are family-dependent. ID 189 means jump reset in canonical XXLDDRace but invisibility-off in TBlock. IDs 190–191 mean jump add/remove in canonical XXLDDRace and modern entity overlay signs in DDNet, so those two IDs alone are not proof of an XXL map.",
        "",
        f"- Inventoried files: {sum(len(v) for v in locations.values())}",
        f"- Unique SHA-256 objects: {len(records)}",
        f"- Unique maps with IDs 176–191: {len(candidates)}",
        f"- Parse failures retained below: {len(errors)}",
        "",
        "## Candidate maps",
        "",
    ]
    for digest, strong, ambiguous, record in sorted(candidates, key=lambda item: (Path(item[3]["path"]).name.lower(), item[0])):
        lines.extend(
            [
                f"### `{Path(record['path']).name}`",
                "",
                f"- SHA-256: `{digest}`",
                f"- Size: `{record['size']}` bytes",
                f"- XXL-family IDs 176–189: `{','.join(map(str, strong)) or 'none'}`",
                f"- Ambiguous IDs 190–191: `{','.join(map(str, ambiguous)) or 'none'}`",
                "- Locations:",
            ]
        )
        lines.extend(f"  - `{location}`" for location in sorted(set(locations[digest])))
        lines.append("")

    lines.extend(["## Parse failures", ""])
    if errors:
        for error in sorted(errors, key=lambda item: item["path"]):
            lines.append(f"- `{error['path']}` ({error['inventory']}): {error['error']}")
    else:
        lines.append("None.")
    lines.append("")

    temporary = OUTPUT.with_name(f".{OUTPUT.name}.tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(OUTPUT)


if __name__ == "__main__":
    main()
