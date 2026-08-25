# DDX

Canonical DDNet 19.9 gameplay source for DDX deployments. Each live server
keeps its own binary, configuration, state, logs, FIFO, and secrets; no live
service executes this mutable source or build tree.

Current additions:

- owner RCON above admin;
- server-side map browser for DDRace, Gores, and the historical archive;
- random votes for map groups and archive search collections;
- `aip` rapid fire;
- owner-controlled grenade bounces;
- target arguments for `super` and `unsuper`.
- explicit compatibility modes for historical XXLDDRace, TBlock, ftk tune
  tiles, Teeworlds 0.5 AiP/XXL hybrid maps, and both known F-DDrace
  combined-teleport encodings.

Maps under `/srv/multi_tas/data/maps` are shared read-only. DDX does not keep a
second copy. Historical maps are extracted on demand into a bounded local
cache.

## Build

```bash
./scripts/build-server.sh
./scripts/install-server.sh ddx-testing ddx-aip-race
./scripts/restart-server.sh ddx-testing
./scripts/restart-server.sh ddx-aip-race
```

Building does not replace the running binary. Install and restart are separate
on purpose. Targets are explicit so a build cannot silently change or restart
an unrelated service. Installation atomically copies the same verified build
into each deployment's private executable path.

Source is the pinned DDNet 19.9 tree in `source/ddnet`. DDX changes live in the
numbered patches. `build/source-map-voting` is generated.

## Historical map compatibility

Historical raw tile IDs conflict across mods and with modern DDNet. DDX never
guesses. Select the source-proven family in the server or embedded map
configuration:

```text
sv_ddx_compat_family 1  # canonical XXLDDRace
sv_ddx_compat_family 2  # TBlock
sv_ddx_compat_family 3  # ftk XXLDDRace tune/rescue extension
sv_ddx_compat_family 4  # Teeworlds 0.5 game tiles with XXL extras

sv_ddx_tele_family 1    # F-DDrace combined input/output types 93/94
sv_ddx_tele_family 2    # F-DDrace combined input/output types 95/94
```

Zero disables each compatibility family. The map-load log reports legacy IDs
that would otherwise be ignored and records the effective selection. Canonical
XXL behavior covers raw game/front tiles `176–185` and `189–191`; ftk also
covers its per-character tune tiles and rescue override; TBlock keeps its
conflicting assignments separate. Historical clan/skin/member gates use
current helper/mod/admin RCON authority rather than trusting client strings or
importing obsolete password storage.

Family `4` is intentionally map-scoped. It restores the Teeworlds 0.5
directional boosters, freeze-boosters, kick tile, and paired game-layer
teleporters while retaining canonical XXL IDs `176–191`. The server selects
this family automatically only for the verified size and full SHA-256 of the
`Aip_Race_extreme_by_Qwer534--8f4a614b00f319694d877e3ee24ee3bd59cbe549a8eab2670db9ec0504a60ccf`
map. Every other map defaults to family zero and retains modern DDRace tile
meanings unless an identified source family is selected explicitly.

Research provenance, raw source inventories, map scans, family conflicts, and
per-candidate `xfeatures.md` reports are under `archive/xxlddrace/`.

## RCON

Owner login:

```text
rcon_login owner <password>
```

`sv_test_cmds` stays off. Owner can use test commands; normal admin cannot.
Passwords stay in ignored `server/secrets.cfg`.

AIP examples:

```text
aip
aip 100
aip 100 3
```

The delay is milliseconds and rounds to the nearest 20 ms server tick. Bare `aip`
toggles the fastest setting. AIP state survives map changes.

Grenade bounce examples:

```text
grenade_bounces 1
grenade_bounces 3 1
grenade_bounces 0
```

The first argument is the number of extra solid-tile bounces; the optional
second argument is a client ID. Grenades fired with a positive value do not
expire in flight or explode on those extra bounces. Player hits and the first
solid collision after the extra bounces still explode normally. The setting
applies to future shots and survives map changes.

## Archive

`/search` creates persistent vote-menu collections. Each collection has its
own random option. Empty maps are skipped and filename aliases do not add extra
weight.

Archive notes and checksums are in `archive/README.md`. The preparation script
is `scripts/prepare-map-archive.py`.

The service helpers are `status-server.sh`, `start-server.sh`,
`stop-server.sh`, and `restart-server.sh` under `scripts/`; each requires
`ddx-testing` or `ddx-aip-race`.
