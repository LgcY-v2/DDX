# FoxNet Telekinesis

This is a design reference only. DDX does not contain this implementation.

## Observed behavior

- Telekinesis can be active as a custom weapon or an account ability.
- Activating it near the cursor grabs the closest living character within a
  radius scaled by camera zoom; activating it again releases the character.
- The target follows the holder's cursor during the pre-tick phase and has its
  velocity reset.
- Each target can have only one holder. Reverse grabs are rejected.
- A target can opt into Telekinesis immunity.
- When normal show-others visibility is restricted, the target must be on the
  holder's DDRace team unless the holder is super.
- Paused players and spectators can use their spectator cursor position. The
  relationship records whether the grab began in that state.
- Grab and release use the ninja-hit sound and apply a 125 ms vote-action
  delay.

FoxNet stores the target as a client ID. This is simpler and safer across
character respawns than a raw entity pointer, but it supports players only.

## Source map

- Selection, movement, team checks, immunity, spectator handling, and action
  delay:
  [`foxnet/player.cpp`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/player.cpp)
- Target ID and public methods:
  [`player.h`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/player.h)
- Weapon fire integration and death cleanup:
  [`character.cpp`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/entities/character.cpp)
- Grant and immunity commands:
  [`commands.cpp`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/commands.cpp)
- Holder cleanup when a target dies or leaves:
  [`foxnet/gamecontext.cpp`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/gamecontext.cpp)

## DDX implementation notes

FoxNet's player-ID ownership model is the smaller starting point for DDX.
Before implementation, DDX still needs explicit decisions for target consent,
team restrictions, frozen and paused holders, collision-safe destination
clamping, maximum range, release on map change and disconnect, and whether the
feature is granted by RCON, map entities, or a player command. Those rules
should be tested before adding non-character targets.
