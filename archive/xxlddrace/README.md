# XXLDDRace compatibility corpus

This directory records the source and map research used to make DDX a
compatible successor to historical XXLDDRace servers. Raw repositories and
downloads are local research inputs, not build inputs and not live runtime
dependencies.

Ownership is deliberately one-way:

- `sources.tsv` identifies every discovered endpoint and the exact local
  revision when available;
- `primary-sources.tsv` records first-party release/support pages and explicit
  archive gaps;
- `repositories/` contains full upstream Git clones and is ignored by the DDX
  repository;
- `downloads/` contains immutable fetched artifacts and is ignored by the DDX
  repository;
- each candidate clone receives an `xfeatures.md` source audit;
- `scan_maps.py` reads raw entity-layer bytes without applying modern DDNet
  validity rules;
- `map-inventory/` contains deterministic JSON Lines scans and
  `map-compatibility.md` deduplicates candidate maps by full SHA-256;
- only independently reviewed DDX patches may affect a build;
- live servers receive explicit, immutable release artifacts and never execute
  files from this corpus.

Discovery covers exact repository-name searches, the GitHub fork network,
GitHub code search, project/forum links, ecosystem indexes, and feature-name
searches. A source being listed does not imply that its behavior is safe or
desired. Duplicated forks are retained as provenance endpoints but audited by
distinct source-tree identity.

The historical map archive already documented in `../README.md` remains a
separate runtime dataset. It must not be copied merely to create this research
corpus.

Current corpus checkpoint:

- 49 Git repositories have full object connectivity checks and pinned HEAD and
  tree identities in `sources.tsv`;
- every cloned candidate has an `xfeatures.md` raw source inventory covering
  every fetched remote branch, with a separate hand audit for canonical
  XXLDDRace;
- the recovered XXL-Clan download, changelog, 0.6.1, 1.8 beta, 64-player
  support, and 2.0 release pages are recorded as first-party evidence; the six
  historical release attachments and entity-explanation page remain explicit
  archive gaps;
- the xXxDdRaCe derivative and a 2011 xxltomate DDRace support bundle are
  recorded from their surviving forum pages; their three linked archive bodies
  remain explicit availability gaps with per-candidate feature reports;
- recovered TBlock and TDDRace releases, the TDDRace 71-map pack, and two
  protected blmapPepe variants have verified archive hashes in `artifacts.tsv`;
- the AiP-Race author's 2010 release page is retained beside a feature report
  for the exact later archive map: the page calls the original map DDRace,
  while the later hash demonstrably carries canonical XXL-family raw IDs;
- the exact AiP extreme hash currently used for acceptance combines the
  recovered Teeworlds 0.5 paired game-layer teleport encoding below ID 176
  with canonical XXL extras at IDs 176–190; it therefore has an explicit,
  map-scoped family instead of a value-based guess;
- the local download/repository sample contains 991 observed map files, 584
  unique hashes, and 114 unique maps using raw IDs 176–191;
- the authoritative 7.26 GB historical archive remains single-copy under the
  testing deployment. A bounded, block-at-a-time pass scanned all 53,400
  distinct mirror hashes and four verified delta maps, retaining 13,628 broad
  collision candidates and 207 explicit parse failures;
- `historical-map-features.md` lists all 5,015 maps carrying IDs 176–189 and
  records the complete-scan digest and family-assignment cautions.

The reviewed server compatibility contract is in `compatibility-contract.md`.
It records the implemented raw IDs, explicit family selectors, security
substitutions, and behavior that remains research-only.
