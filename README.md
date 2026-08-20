# tee_world_candidate_testing

`tee_world_candidate_testing` is a password-protected DDNet 19.9 DDRace server
for candidate feature testing. It listens publicly on UDP port
`8305` and runs as the `lgcy` user service
`tee-world-candidate-testing-ddnet.service`.

The source is pinned to the official DDNet `19.9` tag. A tracked server-only
patch adds clean, browsable map-vote pages and historical archive search for
unmodified DDNet clients. The
runtime starts on the shared `Tutorial` map with the standard `ddnet`
controller, which advertises the `DDraceNetwork` game type.

The map corpus has one authority: `/srv/multi_tas/data/maps`. This server reads
all 3,511 DDRace, Gores, and root maps directly from that path. It does not copy
or synchronize the corpus. Map votes are rebuilt automatically after every map
change, and random DDRace and Gores choices use the same catalog.

## Layout

- `source/ddnet/` — pinned official DDNet source
- `patches/` — tracked server-only map voting patch
- `build/source-map-voting/` — generated patched source (ignored)
- `build/ddnet-map-voting/` — generated patched build (ignored)
- `build/ddnet/DDNet-Server` — release server build
- `server/` — configuration, logs, FIFO, and SQLite score state
- `warehouse/` — archive documentation and ignored verified runtime data
- `deploy/` — installed user-systemd unit source
- `scripts/` — build and lifecycle commands

## Operations

Run these commands as `lgcy`:

```bash
./scripts/status-server.sh
./scripts/restart-server.sh
./scripts/stop-server.sh
./scripts/start-server.sh
```

Build the pinned source plus the tracked server patch with:

```bash
./scripts/build-server.sh
```

The join and RCON credentials are stored only in the ignored
`server/secrets.cfg` file with mode `0600`. Writable runtime data stays under
`server/`. The command FIFO is `server/run/ddnet-server.fifo`.

`sv_map_vote_catalog 1` republishes the catalog on each map load. RCON can also
run `add_map_catalog_votes` to rebuild it immediately after the shared corpus is
updated. The catalog is immutable while active; run `clear_votes` first only
when intentionally switching back to legacy vote options.

## Historical map search

The Map Archive vote section searches 55,250 historical filenames backed by
47,959 distinct map contents. Search collections are virtual and persistent;
creating one does not extract maps. A selected map is extracted only after its
vote passes, verified by SHA-256, and atomically published into a bounded
content-addressed cache.

Chat syntax:

```text
/search aip race
/search *aip*race*
/search race -test
/search aip race --name AIP Race
```

Separate patterns are all required in any order. `*` matches any text, `?`
matches one character, and a leading `-` excludes a pattern. `--name` consumes
the rest of the command as the optional collection name. Without it, the
server creates a short readable name. Searches require at least two literal
characters, return at most 1,000 unique maps, are rate-limited, and are capped
at 24 persisted collections. RCON can run `clear_map_searches` to clear those
collections deliberately.

See `warehouse/README.md` for archive provenance, immutable checksums, delta
coverage, index generation, and cache ownership.

## Connection

Connect to `51.83.129.176:8305` with DDNet. The server name is
`tee_world_candidate_testing`.
