#!/usr/bin/env python3
"""Scan one representative of every content hash in the historical map archive.

The 7-Zip archive is solid. Members are extracted one solid block at a time,
scanned, and immediately removed, bounding temporary disk use to one block.
Only maps with old/custom tile evidence and parse failures are retained; a
digest commits to the canonical scan result for every content hash.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
from dataclasses import dataclass
from pathlib import Path

sys.dont_write_bytecode = True
from scan_maps import scan


MAP_PATH = re.compile(rb"^(.*)_([0-9a-f]{64})\.map$")
KNOWN_DDNET_TELE = {10, 14, 15, 26, 27, 29, 30, 31, 63}


@dataclass(frozen=True)
class Entry:
    path: bytes
    size: int
    block: int | None

    @property
    def sha256(self) -> str:
        match = MAP_PATH.fullmatch(self.path)
        if match is None:
            raise ValueError(f"archive member lacks a SHA-256 suffix: {self.path!r}")
        return match.group(2).decode("ascii")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def parse_listing(extractor: Path, archive: Path) -> list[Entry]:
    process = subprocess.Popen(
        [str(extractor), "l", "-slt", "-ba", str(archive)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    assert process.stdout is not None and process.stderr is not None
    entries: list[Entry] = []
    record: dict[bytes, bytes] = {}

    def finish() -> None:
        if not record:
            return
        path = record.get(b"Path")
        size = record.get(b"Size")
        if path is None or size is None:
            raise ValueError(f"incomplete 7-Zip listing record: {record!r}")
        if any(byte in path for byte in b"\x00\r\n\t") or b"/" in path or b"\\" in path or path in (b".", b".."):
            raise ValueError(f"unsafe archive member: {path!r}")
        path.decode("utf-8")
        block = record.get(b"Block", b"")
        entries.append(Entry(path, int(size), int(block) if block else None))
        record.clear()

    for raw_line in process.stdout:
        line = raw_line.rstrip(b"\r\n")
        if not line:
            finish()
            continue
        key, separator, value = line.partition(b" = ")
        if not separator:
            raise ValueError(f"unexpected 7-Zip listing line: {line!r}")
        record[key] = value
    finish()
    diagnostics = process.stderr.read()
    return_code = process.wait()
    if return_code != 0 or diagnostics:
        raise RuntimeError(f"7-Zip listing failed ({return_code}): {diagnostics.decode(errors='replace')}")
    return entries


def index_identity(path: Path) -> tuple[str, int]:
    fields: dict[str, str] = {}
    with path.open(encoding="utf-8") as source:
        if source.readline().rstrip("\n") != "TW_MAP_ARCHIVE_INDEX\t1":
            raise ValueError("unsupported historical map index")
        for line in source:
            parts = line.rstrip("\n").split("\t")
            if parts[0] == "M":
                break
            if len(parts) == 2:
                fields[parts[0]] = parts[1]
    return fields["archive_sha256"], int(fields["archive_size"])


def canonical(record: dict[str, object]) -> bytes:
    return (json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def is_candidate(record: dict[str, object]) -> bool:
    if "error" in record:
        return True
    entity_ids: set[int] = set()
    tele_ids: set[int] = set()
    for layer in record["layers"]:  # type: ignore[index]
        for name in ("game", "front"):
            entity_ids.update(map(int, layer.get(name, {})))
        tele_ids.update(map(int, layer.get("tele", {})))
    return bool(entity_ids.intersection(range(128, 192)) or tele_ids - KNOWN_DDNET_TELE)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--extractor", type=Path, required=True)
    parser.add_argument("--index", type=Path, required=True)
    parser.add_argument("--delta-dir", type=Path, required=True)
    parser.add_argument("--work-parent", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()

    expected_hash, expected_size = index_identity(args.index)
    if args.archive.stat().st_size != expected_size or file_sha256(args.archive) != expected_hash:
        raise ValueError("historical archive identity does not match its authoritative index")
    entries = parse_listing(args.extractor, args.archive)
    by_hash: dict[str, Entry] = {}
    for entry in entries:
        previous = by_hash.get(entry.sha256)
        if previous is not None and previous.size != entry.size:
            raise ValueError(f"archive aliases disagree on size for {entry.sha256}")
        by_hash.setdefault(entry.sha256, entry)

    delta_paths = sorted(args.delta_dir.glob("*.map"))
    for path in delta_paths:
        match = MAP_PATH.fullmatch(os.fsencode(path.name))
        if match is None:
            raise ValueError(f"delta map lacks a SHA-256 suffix: {path}")
        digest = match.group(2).decode("ascii")
        if file_sha256(path) != digest:
            raise ValueError(f"delta map hash mismatch: {path}")
        if digest in by_hash:
            raise ValueError(f"delta duplicates archive content: {digest}")

    selected_by_block: dict[int | None, list[Entry]] = collections.defaultdict(list)
    for entry in by_hash.values():
        selected_by_block[entry.block].append(entry)
    for values in selected_by_block.values():
        values.sort(key=lambda entry: entry.path)

    args.work_parent.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix="historical-map-scan.", dir=args.work_parent))
    output_temp = args.output.with_name(f".{args.output.name}.tmp.{os.getpid()}")
    summary_temp = args.summary.with_name(f".{args.summary.name}.tmp.{os.getpid()}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    complete_digest = hashlib.sha256()
    scanned = candidates = failures = 0
    peak_batch_bytes = 0

    try:
        with output_temp.open("xb") as output:
            for block in sorted(selected_by_block, key=lambda value: -1 if value is None else value):
                batch_entries = selected_by_block[block]
                batch = work / f"block-{block if block is not None else 'none'}"
                batch.mkdir()
                listfile = work / f"block-{block if block is not None else 'none'}.txt"
                listfile.write_bytes(b"\n".join(entry.path for entry in batch_entries) + b"\n")
                command = [
                    str(args.extractor),
                    "x",
                    "-y",
                    "-bd",
                    "-bb0",
                    "-scsUTF-8",
                    f"-o{batch}",
                    str(args.archive),
                    f"@{listfile}",
                ]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                if result.returncode != 0:
                    raise RuntimeError(
                        f"7-Zip extraction failed for block {block} ({result.returncode}): "
                        f"{result.stderr.decode(errors='replace')[-4000:]}"
                    )
                batch_bytes = sum(entry.size for entry in batch_entries)
                peak_batch_bytes = max(peak_batch_bytes, batch_bytes)
                for entry in batch_entries:
                    path = batch / entry.path.decode("utf-8")
                    if not path.is_file() or path.stat().st_size != entry.size:
                        raise ValueError(f"missing or size-mismatched extracted member: {entry.path!r}")
                    try:
                        record = scan(path)
                        digest = str(record["sha256"])
                    except Exception as error:
                        digest = file_sha256(path)
                        record = {"error": str(error)}
                        failures += 1
                    if digest != entry.sha256:
                        raise ValueError(f"extracted member hash mismatch: {entry.path!r}")
                    record["path"] = f"archive://{expected_hash}/{urllib.parse.quote_from_bytes(entry.path, safe='-._~')}"
                    record["sha256"] = digest
                    record["size"] = entry.size
                    encoded = canonical(record)
                    complete_digest.update(encoded)
                    scanned += 1
                    if is_candidate(record):
                        output.write(encoded)
                        candidates += 1
                output.flush()
                os.fsync(output.fileno())
                shutil.rmtree(batch)
                listfile.unlink()
                print(f"block={block} scanned={scanned} candidates={candidates} failures={failures}", flush=True)

            for path in delta_paths:
                digest = file_sha256(path)
                try:
                    record = scan(path)
                except Exception as error:
                    record = {"error": str(error)}
                    failures += 1
                record["path"] = f"delta://{digest}/{urllib.parse.quote(path.name, safe='-._~')}"
                record["sha256"] = digest
                record["size"] = path.stat().st_size
                encoded = canonical(record)
                complete_digest.update(encoded)
                scanned += 1
                if is_candidate(record):
                    output.write(encoded)
                    candidates += 1
            output.flush()
            os.fsync(output.fileno())

        summary = {
            "schema": 1,
            "archive_sha256": expected_hash,
            "archive_size": expected_size,
            "archive_members": len(entries),
            "archive_unique_hashes": len(by_hash),
            "delta_maps": len(delta_paths),
            "scanned_unique_hashes": scanned,
            "candidate_records": candidates,
            "parse_failures": failures,
            "peak_temporary_batch_bytes": peak_batch_bytes,
            "complete_scan_sha256": complete_digest.hexdigest(),
        }
        with summary_temp.open("xb") as output:
            output.write(json.dumps(summary, indent=2, sort_keys=True).encode("utf-8") + b"\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(output_temp, args.output)
        os.replace(summary_temp, args.summary)
    finally:
        shutil.rmtree(work, ignore_errors=True)
        for temporary in (output_temp, summary_temp):
            if temporary.exists():
                temporary.unlink()
    return 0


if __name__ == "__main__":
    sys.exit(main())
