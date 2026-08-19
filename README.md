# tee_world_candidate_testing

`tee_world_candidate_testing` is a password-protected DDNet 19.9 DDRace server
for candidate feature testing. It listens publicly on UDP port
`8305` and runs as the `lgcy` user service
`tee-world-candidate-testing-ddnet.service`.

The source is pinned to the official DDNet `19.9` tag. The runtime starts on
the bundled `Tutorial` map with the standard `ddnet` controller, which
advertises the `DDraceNetwork` game type.

## Layout

- `source/ddnet/` — pinned official DDNet source
- `build/ddnet/DDNet-Server` — release server build
- `server/` — configuration, startup map, logs, FIFO, and SQLite score state
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

Build the pinned server source with:

```bash
./scripts/build-server.sh
```

The join and RCON credentials are stored only in the ignored
`server/secrets.cfg` file with mode `0600`. Writable runtime data stays under
`server/`. The command FIFO is `server/run/ddnet-server.fifo`.

## Connection

Connect to `51.83.129.176:8305` with DDNet. The server name is
`tee_world_candidate_testing`.
