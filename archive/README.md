# Historical map archive

The live archive, delta files, generated index and metadata, source listings,
and locally extracted 7-Zip tool are runtime data and intentionally ignored by
Git. They are owned by the candidate server and must not be copied into Multi
TAS or another service.

The authoritative requested catalog is Heinrich5991's `LISTING`: 55,250
historical filenames representing 47,959 distinct SHA-256 map contents. The
tee.world `maps.7z` mirror contains 47,955 of those distinct contents. Four
dot-prefixed `.Rudolftopia` maps omitted by the archive are stored as a
SHA-256-verified delta. Filename-only encoding aliases resolve to existing
content hashes and do not create duplicate files.

Runtime paths:

- `source/maps.7z` — immutable compressed mirror archive;
- `delta/` — the four verified missing contents;
- `index/maps-v1.tsv` — deterministic, percent-encoded runtime index;
- `index/map-metadata-v1.tsv` — content-level archive-date metadata;
- `metadata/` — immutable Heinrich and tee.world source listings used to
  reproduce the index and metadata;
- `tools/7zip-26.00/` — extracted Ubuntu 7zip package, not system-installed;
- `manifest.sha256` — immutable runtime bytes checked before every server start;
- `../server/maps/archive/` — bounded 2 GiB/256-map lazy cache.

Regenerate both index files with `scripts/prepare-map-archive.py`. The
command must be given the tee.world directory index, Heinrich `LISTING`,
Heinrich's visible map-directory index, archive, delta directory, and exact
7-Zip executable. It refuses unsafe members, duplicate members, size or hash
gaps, invalid dates, mismatched authorities, or a delta that does not exactly
repair the requested catalog.

Heinrich's visible directory provides file modification dates for 55,204 of
55,250 names and 47,942 of 47,959 distinct contents. Identical content can
appear under aliases with different dates, so the metadata stores the earliest
visible alias date for that content. This prevents a later alias from making
old bytes appear new. The remaining 17 contents use an explicit unknown date
and always appear last in either date direction. These are archive file dates,
not asserted creation or release dates.

Current immutable identities:

- archive bytes: `7265074525`;
- archive SHA-256: `e8c0f3c9b2d13664def818794680a3e411f358927fdbe00d8fb33a4c1b0c8961`;
- Heinrich `LISTING` SHA-256: `3e92ac774f931892c2be3dd9a1753fb4a894ef7552f96de6a1dac951b4a3dd42`;
- Heinrich directory SHA-256: `be12153590467323ded87e659355bd377a6536897921e108cde9b09ae42e4405`;
- generated index SHA-256: `a984c6aff2af954f25ac49c5694534175f90b55ae84833948e80efb71d446d79`;
- generated metadata SHA-256: `430fa4eefea661a39c755754b227f61fb5366f41abad6049fb8708707cebfeb7`.
