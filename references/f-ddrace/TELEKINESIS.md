# F-DDrace Telekinesis

This is a design reference only. DDX does not contain this implementation.

## Observed behavior

- Telekinesis is an extended weapon represented to stock clients as a ninja.
- Firing near the cursor grabs the closest eligible entity; firing again
  releases it.
- A held entity follows the cursor every server tick and has its velocity set
  to zero.
- Eligible targets are other characters, uncarried flags, pickup drops, money,
  helicopters, and spiders.
- A target can have only one holder. Self-grabs, reverse character grabs,
  snake characters, and carried flags are rejected.
- By default, line collision is checked both when grabbing and moving. The
  target is clamped to reachable air instead of being placed inside a block.
- The hold is released when the holder switches weapon, freezes, pauses, or
  loses the target. Entity reset and destruction also clear the holder's
  reference.
- Grab and release use the ninja-hit sound. The fire delay is 125 ms.

## Source map

- Weapon ID and stock-client weapon mapping:
  [`weapons_ex.h`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/engine/shared/weapons_ex.h)
- Grant and revoke commands:
  [`ddracecommands.h`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/ddracecommands.h) and
  [`ddracecommands.cpp`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/ddracecommands.cpp)
- Target acquisition, collision checks, cursor following, and release rules:
  [`character.cpp`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/entities/character.cpp)
- Exclusive target ownership cleanup:
  [`gameworld.cpp`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/gameworld.cpp)
- Movable non-character interface:
  [`advanced_entity.h`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/entities/interactive/advanced_entity.h)
- Tuning and safety switches:
  [`tuning.h`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/tuning.h) and
  [`variables.h`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/variables.h)

Relevant controls are `telekinesis_fire_delay`,
`sv_telekinesis_allow_blocks`, `sv_tele_weapon_through_room_vip`, and
`sv_telerifle_telekinesis_nerf`.

## DDX implementation notes

A first DDX version should keep one authoritative holder-to-target relation,
clear it from every target lifecycle exit, and validate collision on every
movement tick. Stable entity handles are safer than retaining an unchecked raw
pointer across resets. Player-only support can ship before movable objects;
each additional target type needs an explicit position, velocity, collision,
visibility, team, and destruction contract.
