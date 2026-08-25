# DDX historical map compatibility research contract

This records recovered source semantics and the boundary between the passive
research corpus and DDX runtime behavior. A repository, map, or table appearing
here never enables code automatically. Only independently accepted behavior in
the numbered DDX patch stack is executable.

Production acceptance covers only the legacy teleport behavior and exact-map
race primitives described below. The extra entity-tile tables remain research
evidence and are not a supported feature contract. See
[`../../docs/LEGACY_MAP_COMPATIBILITY.md`](../../docs/LEGACY_MAP_COMPATIBILITY.md).

## Selection and failure behavior

- `sv_ddx_tele_family 0` keeps modern DDNet teleport semantics.
- Tele family `1` is the fokkonaut/xuilan `93` normal, `94` evil encoding.
- Tele family `2` is the nameless/uvi `95` normal, `94` evil encoding.
- Tele family `3` is the recovered XXL standard normal, evil, and checkpoint
  behavior.
- Unknown selector values fail closed to modern teleports. Map loading logs the
  effective profile once.
- No automatic inference reinterprets modern or conflicting raw ranges.

## Teeworlds 0.5 AiP hybrid layout

The automatic game-layer profile is limited to a map with size 107225 and
SHA-256
`8f4a614b00f319694d877e3ee24ee3bd59cbe549a8eab2670db9ec0504a60ccf`.
The map is loaded as
`Aip_Race_extreme_by_Qwer534--8f4a614b00f319694d877e3ee24ee3bd59cbe549a8eab2670db9ec0504a60ccf`.

- IDs `5`, `6`, and `8` are the low-strength boosters present in the map.
- IDs `9` and `11` retain freeze and unfreeze behavior.
- IDs `12–15` are the original high-strength directional boosters.
- IDs `21–23` are the freeze boosters present in the map.
- Odd IDs `35–189` are teleport outputs and even IDs `36–190` are their
  paired inputs. Entering an input preserves velocity and weapons and retracts
  the tee's own hook.
- The source-defined down boost `7`, kick `10`, and freeze-up boost `24` are
  absent and inactive.

The map-owned profile is rebuilt on every successful load and never mutates
the configured selector. Every other map keeps modern game-layer meanings.
DDX does not infer a family from tile values because the raw ranges conflict
with modern DDRace checkpoints, stoppers, and control tiles.

## Recovered canonical XXLDDRace and ftk inventory

This table records one recovered canonical XXL ID layout. The exact 0.5 map
profile above assigns different paired-teleport meanings to IDs `176–190`.
The table is not a list of supported DDX features.

| Raw ID | Behavior |
| ---: | --- |
| 176 | Toggle animated rainbow body and feet colors. |
| 177 | Toggle full-auto ordinary weapons with one-tenth bounded reload delays. |
| 178 | Require current DDX admin authority. |
| 179 | Require current DDX helper-or-higher authority. |
| 180 | Toggle modern super state and restore the previous team on exit. |
| 181 | Toggle the historical heavy-hammer force (`m_HammerType = 3`, producing the old four-times directional term). |
| 182 | Toggle snapshot invisibility; self, authenticated controllers, and demos retain visibility. |
| 183 | Toggle the historical death-particle blood trail. |
| 184 | Clear tile-owned cosmetic, rapid-fire, hammer, rescue, invisibility, and super state. |
| 185 | Remove ninja; optional velocity reset is explicit. |
| 189 | Set maximum jumps to two. |
| 190 | Add one jump, bounded to the network field. |
| 191 | Remove one jump, bounded at zero. |

The recovered ftk source also assigns these raw values:

- `0x80–0x87`: air-jump impulse;
- `0x88–0x8a`: laser reach;
- `0x8b–0x8d`: laser bounce count;
- `0x90–0x93`: hook length;
- `0x94–0x96`: ground control speed;
- `0x97–0x9a`: air control speed;
- `0x9b–0x9d`: ground jump impulse;
- `0x9e/0x9f`: player collision;
- `0xa0–0xa7`: gravity;
- `0xa8–0xaa`: ground friction;
- `0xab–0xad`: air friction;
- `0xae/0xaf`: player hooking;
- `0xba/0xbb`: enable/disable rescue for that character.

Any future tune behavior requires its own current DDX ownership and mapping
contract. The recovered path remains deferred with the extra entity-tile work.

## Recovered TBlock layout

The archived TBlock source assigns raw IDs `164`, `166–168`, and `176–189`.
Those IDs conflict with canonical XXLDDRace. Old clan, skin, and member-string
gates are not a safe DDX authorization mechanism because those strings are
client-controlled.

## Teleports

Canonical XXL maps use standard tele types `10`, `26`, `27`, and `29–31`.
With `sv_ddx_tele_family 3`, DDX retains the source behavior for normal, evil,
and checkpoint teleports: normal and checkpoint teleports keep velocity and
weapons and retract the tee's own hook; evil teleports zero velocity, preserve
weapons, and release hooks; super bypasses evil but not canonical normal or
checkpoint teleports.

F-DDrace combined input/output tiles are registered as both an input and an
output. Selection excludes the tile currently occupied, a single-tile set is
a no-op, and per-character entry state prevents immediate loops until the tee
leaves the combined teleporter.

## Security and ownership requirements

- Historical credential files, password hashes, numeric auth ranks, and
  client-supplied clan/skin trust are not imported.
- Accepted compatibility state belongs to one map profile or character and is
  rebuilt or cleared at explicit lifecycle boundaries.
- Compatibility is off by default, so modern maps keep their existing
  meanings.
- Research repositories, archives, maps, and generated reports are passive
  inputs and are not runtime dependencies.

## Deliberately research-only

The entity-tile tables above, candidate account economies, shops,
city/minigame systems, bots, cheats, obsolete clients, old SQL/authentication
implementations, and community policy remain documented research. Every
future DDX feature requires a separate product decision and a complete native
contract before it enters the supported patch stack.
