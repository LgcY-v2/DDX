# DDX baseline

Every server advertised as `DDX` must include this authorization layer. It is
platform behavior, not an optional gameplay feature.

## Owner RCON

DDX adds an internal `owner` role above DDNet's `admin` role. Owner inherits
admin commands and receives two capabilities that lower roles cannot acquire:

- commands marked `CMDFLAG_OWNER`;
- commands marked `CMDFLAG_TEST` while `sv_test_cmds` remains `0`.

Authenticate from an unmodified DDNet client with:

```text
rcon_login owner <password>
```

Configure the named key only in the ignored `server/secrets.cfg` file:

```text
auth_add owner owner "<password>"
```

The startup configuration may create the owner key. Runtime admin, FIFO, and
dashboard commands cannot create, change, remove, or grant the owner role.
Never place the password in tracked configuration, documentation, service
arguments, or logs.

## Authority rules

Authorization is rank-based and evaluated at command execution:

- owner can manage owner, admin, moderator, helper, and unauthenticated players;
- admin and lower roles cannot directly manage an owner;
- equal and lower ranks retain standard DDNet behavior;
- server-owned startup and runtime work remains trusted system authority.

Player-targeting commands resolve through the shared authorization check.
Engine-owned kick and ban checks, address-based mute operations, forced votes,
and bulk team changes enforce the same hierarchy. A bulk operation skips a
higher-ranked player instead of changing them.

Server-wide admin commands such as map changes and shutdown keep their standard
DDNet access. They can affect every connected player indirectly; they do not
grant owner identity or owner-only commands.

The owner rank exists only inside the server. Network snapshots clamp it to
DDNet's public admin value so stock clients remain compatible.

On DDX Testing, owners also control persistent archive collections. `/search`,
`list_map_collections`, `delete_map_collection`, and
`clear_map_searches confirm` are owner-only. The Call vote menu exposes the
same single-collection deletion path only to authenticated owners and requires
a separate review page before deletion.

## Adding DDX commands

Register an owner-only command with `CMDFLAG_OWNER`. Do not compare passwords,
player names, client IDs, or configuration strings inside a command handler.
Commands that act on another player must use the shared victim path or call
`IServer::CanManageClient` before changing state.

Optional DDX gameplay features may vary by server. This authorization layer
must not vary.

## Required verification

Before deploying a DDX build, verify that:

- owner authentication succeeds through `rcon_login`;
- admin cannot execute test or owner-only commands while `sv_test_cmds` is `0`;
- owner can execute test and owner-only commands;
- admin cannot target an owner through player, address, vote, kick, or ban paths;
- admin cannot create, change, remove, or grant owner credentials;
- the public snapshot never exposes an auth value above `AUTHED_ADMIN`.
