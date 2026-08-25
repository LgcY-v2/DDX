# Legacy map compatibility

DDX retains a small server-side compatibility boundary for source-proven
teleports. It does not promise general XXLDDRace entity-tile compatibility and
does not require a custom client.

## Profile selection and lifecycle

`sv_ddx_tele_family` selects the tele-layer decoder:

| Value | Effective tele-layer behavior |
| ---: | --- |
| `0` | Modern DDNet |
| `1` | F-DDrace combined normal `93`, evil `94` |
| `2` | F-DDrace combined normal `95`, evil `94` |
| `3` | XXL standard normal, evil, and checkpoint behavior |

Every other value is rejected and fails closed to modern semantics. The
rejection and effective profile are logged once when the map loads.

The game-layer Teeworlds 0.5 profile is selected independently and only for a
map of 107225 bytes with full SHA-256
`8f4a614b00f319694d877e3ee24ee3bd59cbe549a8eab2670db9ec0504a60ccf`.
The filename is diagnostic, not identity. A same-name file with different
bytes remains modern; identical bytes under another name select the exact
profile.

The collision layer owns the effective profile and precomputed destinations.
It builds them during map initialization, exposes read-only state to character
ticks, and clears them on unload. Automatic detection never writes the
configured selector. A failed replacement keeps the still-active map and its
profile; a successful replacement constructs a new profile before play.

## Verified Teeworlds 0.5 map

The exact map uses paired game-layer teleports: odd IDs `35–189` are outputs,
and the following even IDs `36–190` are matching inputs. An input chooses
uniformly from its available outputs, preserves velocity and weapons, and
retracts the tee's own hook. A missing output is a no-op.

The map also contains these source-proven race primitives needed by its route:

- `5`, `6`, and `8`: low-strength left, right, and up boosts;
- `9`: three-second freeze;
- `11`: unfreeze;
- `12–15`: high-strength directional boosts;
- `21–23`: left, right, and down boosts with three-second freeze.

The recovered down boost `7`, freeze-up boost `24`, and kick tile `10` do not
occur in the exact map and are inactive. Other old low IDs are consumed as
inert compatibility values so they cannot acquire unrelated modern meanings.
Raw IDs `176–190` on this exact profile remain part of the paired encoding;
they are not interpreted as XXL cheat entities.

## Configured tele-layer families

The two F-DDrace profiles treat every selected normal or evil tile of one
number as both an input and an output. Selection excludes the occupied tile
without retries. One output is a no-op. Per-character entry state suppresses
immediate loops until the tee leaves that number and resets on spawn, death,
team change, reconnect, and map replacement.

F-DDrace normal inputs preserve velocity. Hook and weapon changes follow the
standard DDNet teleport configuration. Evil inputs preserve the recovered
DDNet behavior: they reset velocity and release hooks when old-teleport mode is
off, and apply the configured weapon-loss policy. Super bypasses both kinds.
Modern checkpoint tiles keep modern behavior in these profiles.

The XXL profile applies its recovered standard behavior:

- normal inputs teleport even super tees, preserve velocity and weapons, and
  retract the tee's own hook;
- evil inputs bypass super tees; otherwise they reset velocity, retract the
  tee's own hook, release hooks held by other non-super tees, and preserve
  weapons;
- checkpoint inputs teleport even super tees, preserve velocity and weapons,
  and retract the tee's own hook.

Modern DDNet is the default and control path. Unknown combined types remain
inert; malformed layers are rejected by the existing DDNet map loader; missing,
single, and duplicate destinations stay bounded by the precomputed indexes.
Character ticks perform no map scan, file I/O, logging, retry loop, or
allocation.

## Deferred entity tiles

Historical rainbow, super, AiP/XXL rapid fire, admin or member gates, heavy
hammer, invisibility, blood, clear state, remove ninja, jump control,
per-character tune, rescue, TBlock access, and similar entity tiles are not DDX
runtime features. Recovered definitions remain passive research under
`archive/xxlddrace/`.

The accepted owner command `aip` and ordinary DDNet super behavior are separate
DDX features; their names do not enable historical map tiles.

Future gameplay enters DDX one reviewed feature at a time with explicit
authority, lifecycle, tests, mapping, prediction, fallback, and deployment
contracts. New product-facing features use the AiP name. Historical names stay
in provenance where changing them would obscure the recovered source.
