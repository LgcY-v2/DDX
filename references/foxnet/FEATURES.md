# FoxNet feature reference

Source snapshot:
[`24c9d5b`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984)
on the `master` branch.

FoxNet is a modern DDNet server modification with its custom systems grouped
under `src/game/server/foxnet`.

| Feature | What DDX could reuse or study | Primary source |
| --- | --- | --- |
| Accounts, inventory, and shop | Asynchronous accounts, shared-instance identifiers, currency, levels, expiring inventory items, loot cases, and equippable items | [`components/accounts/`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/components/accounts), [`shop.*`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/components), [`item_registry.*`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet) |
| Custom vote menu | Server-built pages and actions for account, inventory, shop, cosmetics, and ordinary votes | [`votemenu.*`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/components) |
| Cosmetics | Trails, hats, pets, orbiting effects, laser death effects, rainbow parts, custom guns, and prediction compensation | [`cosmetics/`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/cosmetics) |
| Custom movement | Configurable UFO flight, snake movement, player pickup, and spider hook | [`vehicles/`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/vehicles) |
| Custom weapons and drops | Telekinesis, heart gun, lightsaber, portal gun, meteor gun, hammerable weapon drops, and drop-on-death rules | [`entities/`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/entities), [`commands.cpp`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/commands.cpp) |
| Zones and minigames | Freeze, unfreeze, death, check-tele, collision, hide-and-seek, roulette, and money-wheel zones | [`components/zones/`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/components/zones) |
| Multi-map runtime | Load several maps, move players between them, and configure cross-map visibility and interaction | [`gamecontext.cpp`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/gamecontext.cpp) |
| Powerups and persistent tee state | Random map powerups and reconnect/reload state restoration | [`powerup.*`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/components), [`persistent_data.*`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet) |
| Server automation | Event scripts, chat/name detection, synchronized bans, reports, and moderator commands | [`components/scripting/`](https://github.com/FoxNet-DDNet/FoxNet/tree/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/components/scripting), [`commands.cpp`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/game/server/foxnet/commands.cpp) |
| Moving quad tiles and tele-grenade compatibility | The README advertises KoG-compatible moving tiles and tele grenades; their configuration declarations are disabled in the inspected snapshot, so they need a compatibility audit before reuse | [`README.md`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/README.md), [`config_variables_foxnet.h`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/src/engine/shared/config_variables_foxnet.h) |

FoxNet is the closer architectural reference for DDX because it is based on a
newer DDNet tree and isolates most additions below one server namespace.
Telekinesis, vote-menu composition, cosmetics, and zones can be evaluated
independently. Accounts, scripting, reports, and synchronized bans expand the
security and persistence boundary and should remain separate projects.

## License

The source uses the zlib-style terms in
[`license.txt`](https://github.com/FoxNet-DDNet/FoxNet/blob/24c9d5bf2fede71388f4ce5e1f2dfa9c2a408984/license.txt).
Assets, fonts, and languages have separate terms. Copied source must retain the
notice and must be marked as altered.
