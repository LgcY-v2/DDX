# DDX

Private DDNet 19.9 server mod used for testing. The server is `DDX | Testing`
on UDP 8305. It still uses the normal DDRace controller.

Current additions:

- owner RCON above admin;
- server-side map browser for DDRace, Gores, and the historical archive;
- random votes for map groups and archive search collections;
- `aip` rapid fire;
- owner-controlled grenade bounces;
- target arguments for `super` and `unsuper`.

Maps under `/srv/multi_tas/data/maps` are shared read-only. DDX does not keep a
second copy. Historical maps are extracted on demand into a bounded local
cache.

## Build

```bash
./scripts/build-server.sh
./scripts/install-server.sh
./scripts/restart-server.sh
```

Building does not replace the running binary. Install and restart are separate
on purpose.

Source is the pinned DDNet 19.9 tree in `source/ddnet`. DDX changes live in the
numbered patches. `build/source-map-voting` is generated.

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
`stop-server.sh`, and `restart-server.sh` under `scripts/`.
