# Historical map warehouse

The live archive, delta files, generated index, and locally extracted 7-Zip
tool are runtime data and intentionally ignored by Git. They are owned by the
candidate server and must not be copied into Multi TAS or another service.

The authoritative requested catalog is Heinrich5991's `LISTING`: 55,250
historical filenames representing 47,959 distinct SHA-256 map contents. The
tee.world `maps.7z` mirror contains 47,955 of those distinct contents. Four
dot-prefixed `.Rudolftopia` maps omitted by the archive are stored as a
SHA-256-verified delta. Filename-only encoding aliases resolve to existing
content hashes and do not create duplicate files.

Runtime paths:

- `archive/maps.7z` — immutable compressed mirror archive;
- `delta/` — the four verified missing contents;
- `index/maps-v1.tsv` — deterministic, percent-encoded runtime index;
- `tools/7zip-26.00/` — extracted Ubuntu 7zip package, not system-installed;
- `manifest.sha256` — immutable runtime bytes checked before every server start;
- `../server/maps/warehouse/` — bounded 2 GiB/256-map lazy cache.

Regenerate the index with `scripts/prepare-map-warehouse.py`. The command must
be given the downloaded mirror directory index, Heinrich `LISTING`, archive,
delta directory, and exact 7-Zip executable. It refuses unsafe members,
duplicate members, hash gaps, or a delta that does not exactly repair the
requested catalog.

Current immutable identities:

- archive bytes: `7265074525`;
- archive SHA-256: `e8c0f3c9b2d13664def818794680a3e411f358927fdbe00d8fb33a4c1b0c8961`;
- Heinrich `LISTING` SHA-256: `3e92ac774f931892c2be3dd9a1753fb4a894ef7552f96de6a1dac951b4a3dd42`;
- generated index SHA-256: `910fbaedfba8873a4bb618edad98b0686dc407fdded8099e7af4ca4e7dfea30f`.
