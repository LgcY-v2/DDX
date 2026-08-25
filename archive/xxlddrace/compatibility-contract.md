# DDX historical map compatibility contract

This is the reviewed boundary between the passive research corpus and DDX
runtime behavior. A repository or map appearing in the corpus never enables
code automatically. Only the numbered DDX patch stack is executable.

## Selection and failure behavior

- `sv_ddx_compat_family 0` disables historical game/front tile semantics.
- Family `1` is canonical XXLDDRace 2.0.
- Family `2` is TBlock's conflicting raw tile layout.
- Family `3` is the ftk XXLDDRace extension, including its per-character tune
  and rescue-control tiles.
- `sv_ddx_tele_family 0` disables combined input/output teleport semantics.
- Tele family `1` is the fokkonaut/xuilan `93` normal, `94` evil encoding.
- Tele family `2` is the nameless/uvi `95` normal, `94` evil encoding.
- Unknown selector values fail closed. Map loading logs unsupported
  historical-looking IDs and the effective configured family.
- No automatic inference reinterprets raw `190/191`, which modern DDNet uses
  for entity-overlay markers, or the conflicting TBlock/ftk ranges.

## Canonical XXLDDRace and ftk layout

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

Family `3` additionally implements the source-exact ftk raw values for:

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

Tune changes are owned per character, sent to that client, and do not mutate
global or zone tuning.

## TBlock layout

Family `2` implements raw IDs `164`, `166–168`, and `176–189` according to the
archived TBlock source. Its raw IDs conflict with canonical XXLDDRace. Old
clan, skin, and member-string gates are deliberately mapped to current DDX
helper/mod/admin authority because those strings are client-controlled.

## Teleports

Canonical XXL maps use standard tele types `10`, `26`, `27`, and `29–31`.
With a historical game family selected, DDX retains the source behavior for
normal, evil, and checkpoint teleports: normal and checkpoint teleports keep
velocity and weapons and retract the tee's own hook; evil teleports zero
velocity and release hooks; super bypasses evil but not canonical normal or
checkpoint teleports.

F-DDrace combined input/output tiles are registered as both an input and an
output. Selection excludes the tile currently occupied, a single-tile set is
a no-op, and per-character entry state prevents immediate loops until the tee
leaves the combined teleporter.

## Security and ownership

- Historical credential files, password hashes, numeric auth ranks, and
  client-supplied clan/skin trust are not imported.
- State belongs to a player or character and is cleared/restored at explicit
  lifecycle boundaries. Ordinary super transitions supersede tile ownership.
- The feature is off by default, so modern maps keep their existing meanings.
- Research repositories, archives, maps, and generated reports are passive
  inputs and are not runtime dependencies.

## Deliberately research-only

Candidate account economies, shops, city/minigame systems, bots, cheats,
obsolete clients, old SQL/authentication implementations, and community
policy remain documented in each `xfeatures.md`. They are not needed to make
XXL maps playable and require separate product decisions before any port.
