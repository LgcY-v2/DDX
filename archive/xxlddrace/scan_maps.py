#!/usr/bin/env python3
"""Inventory raw entity tile IDs in Teeworlds/DDNet map datafiles.

The scanner is intentionally read-only. It reports the bytes stored in entity
layers without applying modern DDNet validity rules, because old mods reused
tile IDs that current DDNet treats as invalid or assigns a different meaning.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import struct
import sys
import tempfile
import zlib
from pathlib import Path


HEADER = struct.Struct("<4s8i")
INT = struct.Struct("<i")
MAX_DIMENSION = 1_000_000
MAX_DATA_SIZE = 2 * 1024 * 1024 * 1024


class MapError(Exception):
    pass


def integers(data: bytes) -> tuple[int, ...]:
    if len(data) % 4:
        raise MapError("integer block is not four-byte aligned")
    return struct.unpack(f"<{len(data) // 4}i", data)


def counts(values: bytes, stride: int, index: int) -> dict[str, int]:
    if stride <= index or len(values) % stride:
        raise MapError("tile data has an invalid size")
    result = collections.Counter(values[index::stride])
    return {str(key): result[key] for key in sorted(result) if key != 0}


def tile_counts(values: bytes, packed: bool) -> dict[str, int]:
    if len(values) % 4:
        raise MapError("tile data has an invalid size")
    if not packed:
        result = collections.Counter(values[0::4])
        return {str(key): result[key] for key in sorted(result) if key != 0}
    result: collections.Counter[int] = collections.Counter()
    for offset in range(0, len(values), 4):
        index, _flags, skip, _reserved = values[offset : offset + 4]
        result[index] += skip + 1
    return {str(key): result[key] for key in sorted(result) if key != 0}


def scan(path: Path) -> dict[str, object]:
    blob = path.read_bytes()
    digest = hashlib.sha256(blob).hexdigest()
    if len(blob) < HEADER.size:
        raise MapError("file is smaller than the datafile header")
    magic, version, size, swaplen, num_types, num_items, num_raw, item_size, data_size = HEADER.unpack_from(blob)
    if magic not in (b"DATA", b"ATAD"):
        raise MapError("unsupported datafile magic")
    if magic == b"ATAD":
        raise MapError("big-endian datafiles are not supported by this scanner")
    if version not in (3, 4):
        raise MapError(f"unsupported datafile version {version}")
    if min(num_types, num_items, num_raw, item_size, data_size) < 0:
        raise MapError("negative datafile size or count")
    if data_size > MAX_DATA_SIZE:
        raise MapError("data section exceeds the safety limit")

    cursor = HEADER.size
    type_bytes = 12 * num_types
    item_offset_bytes = 4 * num_items
    raw_offset_bytes = 4 * num_raw
    raw_size_bytes = 4 * num_raw if version == 4 else 0
    metadata_size = type_bytes + item_offset_bytes + raw_offset_bytes + raw_size_bytes + item_size
    data_start = cursor + metadata_size
    if data_start + data_size != len(blob):
        raise MapError("header sizes do not match the file size")
    if size + 16 not in (len(blob), len(blob) - raw_size_bytes):
        raise MapError("header total size is inconsistent")
    if swaplen + 16 not in (data_start, data_start - raw_size_bytes):
        raise MapError("header swap length is inconsistent")

    cursor += type_bytes
    item_offsets = integers(blob[cursor : cursor + item_offset_bytes])
    cursor += item_offset_bytes
    raw_offsets = integers(blob[cursor : cursor + raw_offset_bytes])
    cursor += raw_offset_bytes
    if version == 4:
        raw_sizes = integers(blob[cursor : cursor + raw_size_bytes])
        cursor += raw_size_bytes
    else:
        raw_sizes = ()
    item_start = cursor

    def raw(index: int) -> bytes:
        if index < 0 or index >= num_raw:
            raise MapError(f"invalid raw data index {index}")
        start = raw_offsets[index]
        end = raw_offsets[index + 1] if index + 1 < num_raw else data_size
        if not 0 <= start <= end <= data_size:
            raise MapError(f"invalid raw data offsets for index {index}")
        value = blob[data_start + start : data_start + end]
        if version == 4:
            expected = raw_sizes[index]
            if not 0 < expected <= MAX_DATA_SIZE:
                raise MapError(f"invalid uncompressed size for index {index}")
            try:
                value = zlib.decompress(value)
            except zlib.error as error:
                raise MapError(f"invalid compressed data at index {index}: {error}") from error
            if len(value) != expected:
                raise MapError(f"uncompressed size mismatch for index {index}")
        return value

    layers: list[dict[str, object]] = []
    for item_index, offset in enumerate(item_offsets):
        end = item_offsets[item_index + 1] if item_index + 1 < num_items else item_size
        if not 0 <= offset < end <= item_size or end - offset < 8:
            raise MapError(f"invalid item offsets for item {item_index}")
        type_and_id, payload_size = struct.unpack_from("<Ii", blob, item_start + offset)
        item_type = type_and_id >> 16
        actual_size = end - offset - 8
        if payload_size != actual_size:
            raise MapError(f"item size mismatch for item {item_index}")
        if item_type != 5:
            continue
        payload = blob[item_start + offset + 8 : item_start + end]
        values = integers(payload)
        if len(values) < 15 or values[1] != 2:
            continue
        tilemap_version, width, height, flags, data_index = values[3], values[4], values[5], values[6], values[14]
        if not 0 <= width <= MAX_DIMENSION or not 0 <= height <= MAX_DIMENSION or width * height > MAX_DIMENSION * MAX_DIMENSION:
            raise MapError(f"invalid tile layer dimensions {width}x{height}")
        layer: dict[str, object] = {
            "item": item_index,
            "version": tilemap_version,
            "width": width,
            "height": height,
            "flags": flags,
        }
        if flags & 1:
            layer["game"] = tile_counts(raw(data_index), tilemap_version >= 4)
        special_fields = (("tele", 2, 18, 2, 1), ("speedup", 4, 19, 6, 2), ("front", 8, 20, 4, 0), ("switch", 16, 21, 4, 1), ("tune", 32, 22, 2, 1))
        for name, layer_flag, field, stride, index_byte in special_fields:
            # Old editors left the unused extension fields uninitialized, so
            # their values are meaningful only for the matching layer flag.
            # Pre-DDRace tilemap items stored special-layer bytes in m_Data.
            if flags & layer_flag:
                extended = len(values) >= 22 and len(values) > field and 0 <= values[field] < num_raw
                special_index = values[field] if extended else data_index
                special = raw(special_index)
                if name == "front" or not extended:
                    layer[name] = tile_counts(special, False)
                else:
                    layer[name] = counts(special, stride, index_byte)
        layers.append(layer)

    return {
        "path": str(path),
        "size": len(blob),
        "sha256": digest,
        "datafile_version": version,
        "layers": layers,
    }


def paths(arguments: list[str]) -> list[Path]:
    result: list[Path] = []
    for argument in arguments:
        path = Path(argument)
        if path.is_dir():
            result.extend(sorted(item for item in path.rglob("*") if item.is_file() and item.suffix.lower() == ".map"))
        else:
            result.append(path)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="map files or directories to scan recursively")
    parser.add_argument("--output", type=Path, help="atomically write JSON Lines here instead of stdout")
    args = parser.parse_args()
    failed = False
    output = sys.stdout
    temporary_name: str | None = None
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(prefix=f".{args.output.name}.", dir=args.output.parent, text=True)
        output = os.fdopen(descriptor, "w", encoding="utf-8")
    try:
        for path in paths(args.paths):
            try:
                record = scan(path)
            except (MapError, OSError) as error:
                failed = True
                record = {"path": str(path), "error": str(error)}
            print(json.dumps(record, sort_keys=True, separators=(",", ":")), file=output)
        if args.output:
            output.flush()
            os.fsync(output.fileno())
            output.close()
            os.replace(temporary_name, args.output)
            temporary_name = None
    finally:
        if args.output and not output.closed:
            output.close()
        if temporary_name is not None:
            os.unlink(temporary_name)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
