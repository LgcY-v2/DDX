# DDX feature ownership

The numbered patches on pinned DDNet
`e5ebaeaad935abc65cf0470a1701877fa258856b` are the executable authority.
Modern DDNet behavior remains the default unless a deployment enables an
optional catalog or a validated teleport profile.

| Capability | Owner and authority | Default and selection | State and lifecycle | Verification | Consumers |
| --- | --- | --- | --- | --- | --- |
| `DDX` server identity | Game controller; server configuration selects the visible name | Compiled in; deployment supplies name, map, and port | No mutable feature state | Clean build and startup identity checks | Testing, AiP-Race |
| Owner RCON role | Engine authentication and shared rank checks | Owner keys come only from the private secrets file; `sv_test_cmds 0` remains the deployment default | Authentication is connection-scoped; credentials remain outside Git | `DdxAuth.*`, runtime owner/admin denial checks | Testing, AiP-Race |
| Target `super` and `unsuper` | Game command victim resolution plus engine rank checks | Registered for DDX; invocation requires sufficient RCON authority | Character/team transition state uses ordinary DDNet lifecycle | `DdxAuth.AuthorizesNumericVictimsBeforeExecution`, runtime command checks | Testing, AiP-Race |
| Sudo spectator movement | Connected player owns the toggle; each command derives its current target and uses shared rank checks | Off until an owner runs `sudo`; only `up`, `down`, `left`, and `right` redirect | Survives map replacement; clears on logout, auth downgrade, disconnect, or restart; target IDs are never retained | `DdxSudo.*`, owner/admin RCON and controlled-client movement checks | Testing, AiP-Race |
| `aip` rapid fire | Owner command; player owns the selected delay | Off until an owner enables it for a player | Player setting survives character and map replacement, then clears on disconnect | `DdxRapidFire.*`, runtime authority and timing checks | Testing, AiP-Race |
| Grenade bounces | Owner command; player owns the future-projectile setting | Zero extra bounces until an owner changes it | Player setting survives map replacement; each projectile copies its launch value | `DdxGrenadeBounce.*`, runtime authority check | Testing, AiP-Race |
| Player handoffs | Engine redirect admission table | Only an explicit redirect creates a bounded, expiring grant | One-use, address-bound in-memory grants; consumed, expired, or cleared on shutdown | `Server.RedirectAdmission*`, protocol reconnect check | Testing, AiP-Race |
| Map archive and browser | Game server owns persistence and per-client pages; Testing overlay owns indexes and cache policy | `sv_map_vote_catalog 0` disables it; Testing enables it and AiP-Race does not; only owners create or delete collections | Static maps build at map load; collection pages build on demand; candidate state is atomically persisted before add/delete publication; extraction remains single-writer with a bounded cache | `MapArchive.*`, `MapVoteCatalog.*`, owner visibility and deletion tests, overlay verification | Testing only |
| Legacy teleports | Collision owns immutable map profile and destination indexes; character owns only combined-entry suppression | `sv_ddx_tele_family 0` is modern; `1`, `2`, and `3` select proven tele-layer families; exact 0.5 behavior uses full hash and size | Built once per map, cleared on unload; character entry state resets on character/team lifecycle | `DdxLegacyTeleport.*`, isolated reload tests, real-client exact-map and generated-family routes | Testing when selected; AiP-Race remains modern |

Historical entity tiles for rainbow, super, AiP/XXL rapid fire, access gates,
heavy hammer, invisibility, blood, state clearing, ninja removal, jump control,
per-character tuning, rescue, and TBlock behavior are research-only. They have
no runtime selector, state owner, deployment consumer, or supported test.
