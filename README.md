# DDX

Canonical DDNet 19.9 server source for DDX. The source repository contains the
complete DDX capability set; each deployment enables only the features it
needs and keeps its own binary, configuration, state, logs, FIFO, and secrets.
No live service executes this mutable source or build tree.

## DDX additions to DDNet 19.9

The numbered patch stack is the authority for this inventory:

- the `DDX` gametype name;
- an owner RCON role above admin, including owner-only commands and test-command
  access while `sv_test_cmds` remains disabled for lower roles;
- target arguments for `super` and `unsuper` with rank-aware authorization;
- `aip` rapid fire with an owner-selected delay and persistent player setting;
- owner-controlled grenade bounces for future projectiles;
- bounded, one-use admission grants for same-address DDNet player handoffs;
- a server-side map browser for DDRace, Gores, and the historical archive;
- archive search collections, random map choices, verified extraction, bounded
  caching, and a map-load cooldown;
- source-proven compatibility for legacy teleport encodings needed to test old
  maps, including the verified Teeworlds 0.5 paired game-layer encoding and the
  two known F-DDrace combined input/output encodings, plus recovered XXL
  normal, evil, and checkpoint teleport semantics.

Archive browsing and historical compatibility are optional server features.
For example, the fixed AiP-Race deployment disables map voting and archive
access while using the same DDX executable.

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

DDX supports legacy teleport adapters so old candidate maps can remain
playable with a stock DDNet client. Historical raw IDs conflict across mods and
with modern DDNet, so compatibility is selected from source evidence or an
exact map identity; raw tile values alone are never enough.

The supported compatibility boundary is:

```text
sv_ddx_tele_family 1    # F-DDrace combined input/output types 93/94
sv_ddx_tele_family 2    # F-DDrace combined input/output types 95/94
sv_ddx_tele_family 3    # XXL normal, evil, and checkpoint teleport semantics
```

Zero keeps modern DDNet teleport semantics. Any other value is rejected and
also uses modern semantics; the server records the rejected selector once at
map load. The verified
`Aip_Race_extreme_by_Qwer534--8f4a614b00f319694d877e3ee24ee3bd59cbe549a8eab2670db9ec0504a60ccf`
map also uses its Teeworlds 0.5 paired game-layer teleport encoding. The server
selects that profile from the map's full SHA-256 and size; the filename is not
part of the identity. The profile is rebuilt for every map and cannot alter
the configured selector or any map loaded before or after it.

Historical rainbow, super, AiP/XXL rapid-fire, admin/member, heavy-hammer,
invisibility, blood, clear-state, remove-ninja, and jump-control entity tiles
are not part of the supported DDX runtime contract. Their recovered definitions
remain research evidence for possible features. DDX will add selected features
one at a time with their own server behavior, tests, mapping contract, and,
when necessary, client/editor support.

The implemented compatibility boundary is documented in
[`docs/LEGACY_MAP_COMPATIBILITY.md`](docs/LEGACY_MAP_COMPATIBILITY.md). The
capability ownership matrix is in
[`docs/DDX_FEATURE_MATRIX.md`](docs/DDX_FEATURE_MATRIX.md). The cleanup and
deployment contract is retained in
[`docs/goals/CLEAN_DDX_FOUNDATION.md`](docs/goals/CLEAN_DDX_FOUNDATION.md).

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
