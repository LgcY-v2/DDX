# F-DDrace feature reference

Source snapshot:
[`c2666ef`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643)
on the `F-DDrace` branch.

F-DDrace is an open-world DDNet/Teeworlds mod. Its own README and the source
areas below identify these distinctive systems.

| Feature | What DDX could reuse or study | Primary source |
| --- | --- | --- |
| Accounts and economy | Persistent level, experience, money, statistics, login recovery, banking, payments, and farming rules | [`misc/accounts.*`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/misc), [`houses/`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/houses) |
| Shops and social spaces | Map-integrated shops, houses, a tavern, purchasable upgrades, and grog | [`houses/`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/houses) |
| Plots and in-game editing | Rentable plots with pickups, walls, doors, speedups, teleporters, selection, copy, move, save, and load tools | [`misc/plots.*`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/misc), [`entities/map/draweditor/`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/entities/map/draweditor) |
| Custom vote menu | Categories, collapsible entries, toggles, value entry through vote reasons, prefixes, and combined elements | [`gamecontext.cpp`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/gamecontext.cpp) |
| Minigames | Saved-and-restored player state around survival, configurable 1vs1 arenas, and the Durák card game | [`minigames/`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/minigames) |
| Movable objects and custom weapons | Hookable flags, weapon and money drops, portals, tele weapons, Telekinesis, lightsabers, projectile variants, helicopters, and spiders | [`entities/`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/entities), [`weapons_ex.h`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/engine/shared/weapons_ex.h) |
| Persistent live state | Money drops, plots, and complete tee state survive controlled restarts and reconnects | [`misc/savedtees.*`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/misc) |
| Server-side language selection | Per-player translations with server defaults and language suggestions | [`datasrc/languages/`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/datasrc/languages) |
| Protocol and scale work | DDNet and 0.7 translation plus support for up to 128 players | [`readme.md`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/readme.md) |
| Custom tiles and server dummies | New map entities, per-player tune locks, redirect tiles, plot tiles, vehicles, and map-specific bots | [`mapitems.h`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/mapitems.h), [`entities/dummy/`](https://github.com/fokkonaut/F-DDrace/tree/c2666efdef164e7fc6fda397f3a77491bb8b3643/src/game/server/entities/dummy) |

The strongest near-term references for DDX are isolated mechanics that do not
require the account or open-world stack: Telekinesis, custom weapons, movable
entities, and focused vote-menu components. Accounts, plots, and persistent
world state require separate storage, security, migration, and abuse designs.

## License

The source uses the zlib-style terms in
[`license.txt`](https://github.com/fokkonaut/F-DDrace/blob/c2666efdef164e7fc6fda397f3a77491bb8b3643/license.txt).
Content under `data` and `datasrc` has separate CC BY-SA 3.0 and font terms.
Copied source must retain the notice and must be marked as altered.
