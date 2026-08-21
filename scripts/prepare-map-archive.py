#!/usr/bin/env python3
"""Verify the historical map archive and build its runtime search index."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import os
import re
import subprocess
import sys
import unicodedata
import urllib.parse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


MAP_PATH_RE = re.compile(rb"^(.*)_([0-9a-f]{64})\.map$")
HTML_ENTRY_RE = re.compile(rb'href="([^"]+\.map)".*?</a>\s+\S+\s+\S+\s+(\d+)\s*$')
HEINRICH_DIRECTORY_ENTRY_RE = re.compile(
    rb'href="([^"]+\.map)".*?</a>\s+'
    rb'(\d{2})-([A-Z][a-z]{2})-(\d{4})\s+(\d{2}):(\d{2})\s+(\d+)\s*$'
)
MONTHS = {
    b"Jan": 1,
    b"Feb": 2,
    b"Mar": 3,
    b"Apr": 4,
    b"May": 5,
    b"Jun": 6,
    b"Jul": 7,
    b"Aug": 8,
    b"Sep": 9,
    b"Oct": 10,
    b"Nov": 11,
    b"Dec": 12,
}


@dataclass(frozen=True)
class ArchiveEntry:
    path: bytes
    size: int
    block: int | None

    @property
    def match(self) -> re.Match[bytes]:
        match = MAP_PATH_RE.fullmatch(self.path)
        if match is None:
            raise ValueError(f"archive member has no name/hash suffix: {self.path!r}")
        return match

    @property
    def name_bytes(self) -> bytes:
        return self.match.group(1)

    @property
    def sha256(self) -> str:
        return self.match.group(2).decode("ascii")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        while chunk := source.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def percent_encode(value: bytes) -> str:
    return urllib.parse.quote_from_bytes(value, safe="-._~")


def clean_display_name(value: bytes) -> str:
    text = value.decode("utf-8", errors="replace")
    text = "".join(" " if unicodedata.category(char).startswith("C") else char for char in text)
    text = " ".join(text.split())
    return text or "Untitled"


def parse_archive(extractor: Path, archive: Path) -> list[ArchiveEntry]:
    command = [str(extractor), "l", "-slt", "-ba", str(archive)]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert process.stdout is not None
    assert process.stderr is not None

    entries: list[ArchiveEntry] = []
    record: dict[bytes, bytes] = {}

    def finish_record() -> None:
        if not record:
            return
        path = record.get(b"Path")
        size = record.get(b"Size")
        if path is None or size is None:
            raise ValueError(f"incomplete 7-Zip listing record: {record!r}")
        if any(byte in path for byte in b"\x00\r\n\t"):
            raise ValueError(f"archive member contains a control separator: {path!r}")
        if b"/" in path or b"\\" in path or path in (b".", b".."):
            raise ValueError(f"archive member is not a safe root filename: {path!r}")
        block_text = record.get(b"Block", b"")
        entries.append(ArchiveEntry(path, int(size), int(block_text) if block_text else None))
        record.clear()

    for raw_line in process.stdout:
        line = raw_line.rstrip(b"\r\n")
        if not line:
            finish_record()
            continue
        key, separator, value = line.partition(b" = ")
        if not separator:
            raise ValueError(f"unexpected 7-Zip listing line: {line!r}")
        record[key] = value
    finish_record()

    stderr = process.stderr.read()
    return_code = process.wait()
    if return_code != 0:
        raise RuntimeError(f"7-Zip listing failed ({return_code}): {stderr.decode(errors='replace')}")
    if stderr:
        raise RuntimeError(f"7-Zip wrote unexpected listing diagnostics: {stderr.decode(errors='replace')}")
    return entries


def parse_mirror_listing(path: Path) -> dict[bytes, int]:
    result: dict[bytes, int] = {}
    for line_number, line in enumerate(path.read_bytes().splitlines(), start=1):
        match = HTML_ENTRY_RE.search(line)
        if match is None:
            continue
        href = html.unescape(match.group(1).decode("ascii"))
        member = urllib.parse.unquote_to_bytes(href)
        size = int(match.group(2))
        if member in result:
            raise ValueError(f"duplicate mirror member on line {line_number}: {member!r}")
        result[member] = size
    return result


def parse_heinrich_listing(path: Path) -> list[bytes]:
    entries = []
    for line_number, line in enumerate(path.read_bytes().splitlines(), start=1):
        if not line:
            continue
        if MAP_PATH_RE.fullmatch(line) is None:
            raise ValueError(f"invalid Heinrich listing entry on line {line_number}: {line!r}")
        entries.append(line)
    return entries


def parse_heinrich_directory(path: Path) -> dict[bytes, tuple[int, int]]:
    result: dict[bytes, tuple[int, int]] = {}
    for line_number, line in enumerate(path.read_bytes().splitlines(), start=1):
        if b'href="' not in line or b".map" not in line:
            continue
        match = HEINRICH_DIRECTORY_ENTRY_RE.search(line)
        if match is None:
            raise ValueError(f"malformed Heinrich directory entry on line {line_number}: {line!r}")
        href = html.unescape(match.group(1).decode("ascii"))
        member = urllib.parse.unquote_to_bytes(href)
        if MAP_PATH_RE.fullmatch(member) is None:
            raise ValueError(f"invalid Heinrich directory member on line {line_number}: {member!r}")
        day = int(match.group(2))
        month = MONTHS.get(match.group(3))
        year = int(match.group(4))
        hour = int(match.group(5))
        minute = int(match.group(6))
        if month is None:
            raise ValueError(f"invalid Heinrich directory month on line {line_number}")
        try:
            timestamp = dt.datetime(year, month, day, hour, minute)
        except ValueError as error:
            raise ValueError(f"invalid Heinrich directory date on line {line_number}: {error}") from error
        if not 2000 <= timestamp.year <= 2100:
            raise ValueError(f"implausible Heinrich directory date on line {line_number}: {timestamp}")
        archive_date = int(timestamp.strftime("%Y%m%d%H%M"))
        size = int(match.group(7))
        if member in result:
            raise ValueError(f"duplicate Heinrich directory member on line {line_number}: {member!r}")
        result[member] = (archive_date, size)
    if not result:
        raise ValueError("Heinrich directory listing contains no map entries")
    return result


def write_atomic(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp.{os.getpid()}")
    with temporary.open("xb") as output:
        output.write(content)
        output.flush()
        os.fsync(output.fileno())
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--extractor", type=Path, required=True)
    parser.add_argument("--mirror-listing", type=Path, required=True)
    parser.add_argument("--heinrich-listing", type=Path, required=True)
    parser.add_argument("--heinrich-directory-listing", type=Path, required=True)
    parser.add_argument("--delta-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--metadata-output", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()

    for required in (
        args.archive,
        args.extractor,
        args.mirror_listing,
        args.heinrich_listing,
        args.heinrich_directory_listing,
    ):
        if not required.is_file():
            parser.error(f"required file does not exist: {required}")
    if not args.delta_dir.is_dir():
        parser.error(f"required delta directory does not exist: {args.delta_dir}")

    archive_size = args.archive.stat().st_size
    archive_sha256 = file_sha256(args.archive)
    mirror_sha256 = file_sha256(args.mirror_listing)
    heinrich_sha256 = file_sha256(args.heinrich_listing)
    heinrich_directory_sha256 = file_sha256(args.heinrich_directory_listing)

    archive_entries = parse_archive(args.extractor, args.archive)
    archive_by_path: dict[bytes, ArchiveEntry] = {}
    for entry in archive_entries:
        if entry.path in archive_by_path:
            raise ValueError(f"duplicate archive member: {entry.path!r}")
        archive_by_path[entry.path] = entry

    mirror_entries = parse_mirror_listing(args.mirror_listing)
    if not mirror_entries:
        raise ValueError("mirror listing contains no map entries")
    archive_pairs = {(entry.path, entry.size) for entry in archive_entries}
    mirror_pairs = set(mirror_entries.items())
    missing_from_archive = sorted(mirror_pairs - archive_pairs)
    extra_in_archive = sorted(archive_pairs - mirror_pairs)

    heinrich_entries = parse_heinrich_listing(args.heinrich_listing)
    if len(set(heinrich_entries)) != len(heinrich_entries):
        raise ValueError("Heinrich listing contains duplicate map entries")
    heinrich_missing_exact = sorted(set(heinrich_entries) - set(archive_by_path))
    archive_by_hash: dict[str, list[ArchiveEntry]] = {}
    for entry in archive_entries:
        archive_by_hash.setdefault(entry.sha256, []).append(entry)
    for content_hash, entries in archive_by_hash.items():
        sizes = {entry.size for entry in entries}
        if len(sizes) != 1:
            raise ValueError(f"archive aliases disagree on size for content hash {content_hash}")
    archive_hashes = set(archive_by_hash)
    heinrich_hashes = {MAP_PATH_RE.fullmatch(entry).group(2).decode("ascii") for entry in heinrich_entries}  # type: ignore[union-attr]
    heinrich_missing_hashes = sorted(heinrich_hashes - archive_hashes)
    heinrich_directory_entries = parse_heinrich_directory(args.heinrich_directory_listing)
    extra_directory_entries = sorted(set(heinrich_directory_entries) - set(heinrich_entries))
    if extra_directory_entries:
        raise ValueError(
            f"Heinrich directory contains {len(extra_directory_entries)} entries absent from its authority listing"
        )

    delta_by_hash: dict[str, tuple[bytes, int]] = {}
    for delta_path in sorted(args.delta_dir.iterdir()):
        if not delta_path.is_file():
            continue
        member = os.fsencode(delta_path.name)
        match = MAP_PATH_RE.fullmatch(member)
        if match is None:
            raise ValueError(f"delta file has no name/hash suffix: {delta_path}")
        expected_hash = match.group(2).decode("ascii")
        actual_hash = file_sha256(delta_path)
        if actual_hash != expected_hash:
            raise ValueError(f"delta hash mismatch for {delta_path}: {actual_hash}")
        if expected_hash in delta_by_hash:
            raise ValueError(f"duplicate delta content hash: {expected_hash}")
        delta_by_hash[expected_hash] = (member, delta_path.stat().st_size)
    uncovered_hashes = sorted(set(heinrich_missing_hashes) - set(delta_by_hash))
    unused_delta_hashes = sorted(set(delta_by_hash) - set(heinrich_missing_hashes))
    if uncovered_hashes or unused_delta_hashes:
        raise ValueError(
            "delta does not exactly repair Heinrich coverage: "
            f"uncovered={len(uncovered_hashes)}, unused={len(unused_delta_hashes)}"
        )

    content_sizes = {
        content_hash: entries[0].size for content_hash, entries in archive_by_hash.items()
    }
    content_sizes.update({content_hash: value[1] for content_hash, value in delta_by_hash.items()})
    dates_by_hash: dict[str, list[int]] = {}
    for member, (archive_date, listed_size) in heinrich_directory_entries.items():
        match = MAP_PATH_RE.fullmatch(member)
        assert match is not None
        content_hash = match.group(2).decode("ascii")
        expected_size = content_sizes.get(content_hash)
        if expected_size is None or expected_size != listed_size:
            raise ValueError(
                f"Heinrich directory size disagrees with verified content {content_hash}: "
                f"listed={listed_size}, verified={expected_size}"
            )
        dates_by_hash.setdefault(content_hash, []).append(archive_date)
    earliest_dates = {
        content_hash: min(dates) for content_hash, dates in dates_by_hash.items()
    }

    indexed_entries: list[tuple[bytes, str, int, str, bytes]] = []
    for alias in heinrich_entries:
        match = MAP_PATH_RE.fullmatch(alias)
        assert match is not None
        name = match.group(1)
        content_hash = match.group(2).decode("ascii")
        exact_archive_entry = archive_by_path.get(alias)
        if exact_archive_entry is not None:
            source_kind = "A"
            source_path = exact_archive_entry.path
            size = exact_archive_entry.size
        elif content_hash in archive_by_hash:
            canonical = min(
                archive_by_hash[content_hash],
                key=lambda entry: (len(entry.path), entry.path),
            )
            source_kind = "A"
            source_path = canonical.path
            size = canonical.size
        else:
            source_kind = "D"
            source_path, size = delta_by_hash[content_hash]
        indexed_entries.append((name, content_hash, size, source_kind, source_path))

    sorted_entries = sorted(
        indexed_entries,
        key=lambda entry: (clean_display_name(entry[0]).casefold(), entry[1], entry[4]),
    )
    lines = [
        "TW_MAP_ARCHIVE_INDEX\t1",
        f"archive_sha256\t{archive_sha256}",
        f"archive_size\t{archive_size}",
        f"authority_listing_sha256\t{heinrich_sha256}",
        f"mirror_listing_sha256\t{mirror_sha256}",
        f"map_entries\t{len(sorted_entries)}",
        f"unique_content\t{len(heinrich_hashes)}",
        "",
    ]
    for name, content_hash, size, source_kind, source_path in sorted_entries:
        display = clean_display_name(name).encode("utf-8")
        if len(display) > 256:
            raise ValueError(f"display name exceeds the runtime limit: {display!r}")
        if len(source_path) > 512:
            raise ValueError(f"source filename exceeds the runtime limit: {source_path!r}")
        lines.append(
            "\t".join(
                (
                    "M",
                    percent_encode(display),
                    content_hash,
                    str(size),
                    source_kind,
                    percent_encode(source_path),
                )
            )
        )
    index_content = ("\n".join(lines) + "\n").encode("ascii")
    write_atomic(args.output, index_content)

    metadata_lines = [
        "TW_MAP_ARCHIVE_METADATA\t1",
        f"authority_listing_sha256\t{heinrich_sha256}",
        f"directory_listing_sha256\t{heinrich_directory_sha256}",
        f"map_entries\t{len(heinrich_entries)}",
        f"dated_entries\t{len(heinrich_directory_entries)}",
        f"unique_content\t{len(heinrich_hashes)}",
        f"dated_content\t{len(earliest_dates)}",
        "date_semantics\tearliest_visible_alias_file_mtime",
        "",
    ]
    for content_hash in sorted(earliest_dates):
        metadata_lines.append(f"D\t{content_hash}\t{earliest_dates[content_hash]:012d}")
    metadata_content = ("\n".join(metadata_lines) + "\n").encode("ascii")
    write_atomic(args.metadata_output, metadata_content)

    block_counts = Counter(entry.block for entry in archive_entries)
    block_bytes = Counter()
    for entry in archive_entries:
        block_bytes[entry.block] += entry.size
    report_lines = [
        "# Map archive preparation report",
        "",
        f"- Archive: `{args.archive}`",
        f"- Archive bytes: `{archive_size}`",
        f"- Archive SHA-256: `{archive_sha256}`",
        f"- Archive members: `{len(archive_entries)}`",
        f"- Distinct content hashes: `{len(archive_hashes)}`",
        f"- Zero-byte members: `{sum(entry.size == 0 for entry in archive_entries)}`",
        f"- Mirror listing SHA-256: `{mirror_sha256}`",
        f"- Mirror directory entries: `{len(mirror_pairs)}`",
        f"- Mirror entries absent from the archive: `{len(missing_from_archive)}`",
        f"- Archive entries absent from the mirror directory: `{len(extra_in_archive)}`",
        f"- Heinrich listing SHA-256: `{heinrich_sha256}`",
        f"- Heinrich aliases indexed: `{len(set(heinrich_entries))}`",
        f"- Heinrich aliases whose exact filename is in the archive: `{len(set(heinrich_entries)) - len(heinrich_missing_exact)}`",
        f"- Heinrich filename aliases resolved by identical content hash: `{len(heinrich_missing_exact) - len(heinrich_missing_hashes)}`",
        f"- Heinrich distinct hashes in the archive: `{len(heinrich_hashes) - len(heinrich_missing_hashes)}`",
        f"- Heinrich distinct hashes repaired by verified delta: `{len(delta_by_hash)}`",
        f"- Heinrich distinct hashes covered in total: `{len(heinrich_hashes)}`",
        f"- Heinrich directory SHA-256: `{heinrich_directory_sha256}`",
        f"- Heinrich directory aliases with a listed date: `{len(heinrich_directory_entries)}`",
        f"- Heinrich distinct hashes with a listed date: `{len(earliest_dates)}`",
        f"- Heinrich distinct hashes without a listed date: `{len(heinrich_hashes) - len(earliest_dates)}`",
        f"- Content hashes whose aliases have different listed dates: `{sum(len(set(dates)) > 1 for dates in dates_by_hash.values())}`",
        f"- Runtime index SHA-256: `{hashlib.sha256(index_content).hexdigest()}`",
        f"- Runtime metadata SHA-256: `{hashlib.sha256(metadata_content).hexdigest()}`",
        "",
        "## Solid blocks",
        "",
        "| Block | Members | Uncompressed bytes |",
        "| ---: | ---: | ---: |",
    ]
    for block in sorted(block_counts, key=lambda value: (-1 if value is None else value)):
        label = "none" if block is None else str(block)
        report_lines.append(f"| {label} | {block_counts[block]} | {block_bytes[block]} |")
    report_lines.append("")
    write_atomic(args.report, "\n".join(report_lines).encode("utf-8"))

    print(f"verified {len(archive_entries)} archive members and wrote {args.output}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, RuntimeError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
