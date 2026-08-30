# Clean and deploy the DDX foundation

Submit this file as one goal:

```text
/goal Clean, verify, publish, and deploy the DDX server foundation exactly as specified in docs/goals/CLEAN_DDX_FOUNDATION.md.
```

## Outcome

Leave DDX with one reproducible server source, clean deployment ownership, and
an intentionally small legacy-map compatibility boundary. Existing DDX
features and ordinary DDNet/DDRace behavior must remain intact. The verified
old-map teleports must keep working. Unsupported historical cheat entity tiles
must no longer be presented or carried as finished DDX features.

Publish the verified repositories and deploy the resulting DDX binary to the
two DDX servers, one at a time, without changing their names, ports, maps,
passwords, voting policy, or unrelated services.

This is an implementation, publication, and production-operation goal. It is
not a client project, a new gameplay feature project, or a general port of
XXLDDRace.

## Read before acting

Read these files completely, in this order:

1. the current owner request that started this goal;
2. `/srv/AGENTS.md`;
3. `/srv/ddx/AGENTS.md`;
4. `/srv/ddx_testing/AGENTS.md`;
5. `/srv/ddx_aip_race/AGENTS.md`;
6. `/srv/ddx_testing/prompt_standard_v2.md`;
7. `/srv/ddx/README.md`;
8. `/srv/ddx/docs/DDX_BASELINE.md`;
9. `/srv/ddx/docs/LEGACY_MAP_COMPATIBILITY.md`;
10. `/srv/ddx/archive/xxlddrace/compatibility-contract.md`;
11. both deployment READMEs, feature manifests, revision pins, manifests,
    sanitized configuration, service templates, and verification scripts;
12. every nearer instruction discovered below a file before changing that
    file.

Apply the general evidence, state-ownership, repository-safety, bounded
100 → 120, checkpoint, adversarial-review, and handoff rules from
`prompt_standard_v2.md`. Its OmniShare-specific visual and product rules do not
apply to this server task. Do not move, delete, commit, or absorb that untracked
file merely because this prompt references it.

Reread the owner request before freezing each phase contract and before the
final production decision. Record a short vision check in the live task status:

- old candidate maps remain playable because their source-proven teleports
  work;
- ordinary DDNet/DDRace maps do not change;
- historical cheat tiles are deferred;
- the main DDX source retains the complete accepted DDX feature set;
- deployments choose features through explicit configuration;
- future gameplay is added one reviewed feature at a time.

## Planning evidence to re-derive

The documentation pass that wrote this goal inspected `/srv/ddx` at commit
`0319ea2`. Do not assume that revision is still current. Fetch and derive the
implementation base again.

At that checkpoint:

- `/srv/ddx` was the clean `LgcY-v2/DDX` source checkout;
- `/srv/ddx_testing` was an older dirty checkout of the same remote with
  deployment edits and unrelated untracked work;
- `/srv/ddx_aip_race` was the clean `LgcY-v2/DDX-AiP-Race` deployment overlay;
- the source was pinned to DDNet 19.9 revision
  `e5ebaeaad935abc65cf0470a1701877fa258856b`;
- DDX changes were owned by the numbered patch stack and applied into an
  ignored generated source tree;
- historical teleport and entity-tile code was mixed across patches 0011 and
  0012;
- raw entity-tile actions were defined for IDs `176–191`, but the ordinary
  collision tile-admission path did not admit those IDs, so their handlers did
  not form a verified end-to-end feature;
- exact-map auto-selection wrote the detected family into the global configured
  selector, creating a map-reload ownership risk that must be reproduced and
  removed;
- the verified Teeworlds 0.5 map profile used size `107225` and SHA-256
  `8f4a614b00f319694d877e3ee24ee3bd59cbe549a8eab2670db9ec0504a60ccf`;
- DDX Testing used UDP 8305 and DDX AiP-Race used UDP 8306;
- KOG Lab and Multi TAS were unrelated live services and read-only for this
  goal.

Recheck all repositories, worktrees, branches, remotes, staged and unstaged
diffs, untracked files, submodules, running units, PIDs, restart counters,
listeners, deployed binary hashes, map hashes, firewall rules, dashboard
catalog entries, recovery inventory, and offsite state before editing.

Do not display or copy the contents of any secret, password, credential hash,
SQLite database, console history, or private runtime file. Compare secrets only
with permissions, ownership, `cmp`, or hashes that are not published.

## Product decisions

These decisions are already made. Do not reopen them without contradictory
runtime or primary-source evidence.

### One source, selectable capabilities

`LgcY-v2/DDX` is the canonical server source. It contains every accepted DDX
capability and one pinned DDNet base. Live servers use the same verified DDX
binary where their platform permits it. Deployment overlays select optional
capabilities through configuration and own their own immutable asset manifest,
revision pin, service contract, secrets, binary, map assets, logs, FIFO, and
state.

Keep the pinned-upstream plus numbered-patch model for this cleanup. It is the
current reproducible build and recovery contract. Clean the authored code in
the patch stack and regenerate patches with repository tooling; never edit the
generated patched source as the authority. A later direct-fork migration needs
its own measured decision and must not be smuggled into this task.

### Teleports are the compatibility boundary

Retain source-proven legacy teleport behavior required to test old maps:

- modern DDNet teleports remain unchanged;
- the verified Teeworlds 0.5 paired game-layer encoding is selected only for
  its exact map profile;
- the two known F-DDrace combined input/output tele-layer encodings remain
  explicit configured profiles;
- normal, evil, checkpoint, hook, velocity, weapon, super, and loop-prevention
  behavior must match the recovered source and accepted runtime evidence;
- an ambiguous or unknown encoding fails closed instead of guessing from raw
  tile IDs.

Keep only additional historical race primitives that are both source-proven
and necessary for an accepted test route to remain playable. Document each
one. Do not use this exception to retain unrelated power, cosmetic, access, or
cheat features.

Effective compatibility is immutable map state. Build it once during map load,
read it during ticks, and clear it during map replacement. Never mutate the
configured selector to record automatic map detection. Loading the verified
legacy map, then a modern map, then the legacy map again must produce the same
three isolated results.

### Historical cheat tiles are deferred

Do not implement or repair historical rainbow, super, AiP/XXL rapid-fire,
admin/member, heavy-hammer, invisibility, blood, clear-state, remove-ninja,
jump-control, per-character tune, rescue, TBlock access, or similar entity
tiles in this goal. Remove or isolate provisional runtime code, configuration,
state, tests, and documentation that falsely makes them part of the supported
contract. Preserve the research inventories and provenance.

The existing owner command `aip` is an accepted DDX feature and must remain.
It is separate from an unsupported historical AiP/XXL map tile. Apply the same
distinction to accepted owner commands and ordinary DDNet super behavior.

### No client work yet

A stock DDNet client is sufficient for the retained server-side teleport
compatibility. Do not create a DDX client, editor fork, entity texture, tile ID,
network message, map conversion, or protocol extension in this goal.

When a selected future feature needs native mapping, it will receive a
coordinated server, shared map-format, prediction, editor, entity-art, protocol,
fallback, and migration contract. New product-facing features use the AiP name.
Historical names remain only in source provenance.

## Repository ownership target

End with these clear owners:

- `/srv/ddx`: canonical `LgcY-v2/DDX` source, research, build, test, install,
  and operator tooling;
- `/srv/ddx_testing`: live DDX Testing deployment contract and runtime, not a
  second mutable DDX source authority;
- `/srv/ddx_aip_race`: live AiP-Race deployment overlay and runtime;
- `/srv/vps-dashboard`: dashboard catalog, controller, recovery, and release
  integration only.

First determine whether a published DDX Testing overlay repository already
exists. If not, prepare `LgcY-v2/DDX-Testing` with the same visibility as
`LgcY-v2/DDX`. It should be as small as the AiP-Race overlay and track only
authored, sanitized, reproducible deployment material. Do not publish maps,
archives, binaries, skins without verified redistribution rights, secrets,
runtime state, logs, FIFOs, dumps, demos, ghosts, teehistorian data, build
trees, transcripts, or unrelated local files.

Do not convert `/srv/ddx_testing` in place by surprise. Before any repository
metadata migration:

1. snapshot the exact staged diff, unstaged diff, branch and ref identities,
   submodule state, ignored and untracked inventory, file ownership, and
   relevant hashes;
2. create a verified Git bundle of every local ref and recoverable patch
   snapshots outside the deployment root in an exact `0700` directory, with
   sensitive artifacts mode `0600`; never publish that recovery bundle or add
   it to a general offsite backup without validating its contents and policy;
3. classify every dirty and untracked path as deployment input, unique source
   work, generated output, runtime data, research asset, or unrelated user
   work;
4. integrate each unique authored change into its owning repository or retain
   it unchanged in the recovery snapshot;
5. prepare, test, commit, and push the new overlay from a separate directory;
6. prove the live service and recovery workflow do not depend on the old Git
   metadata or redundant source checkout;
7. move, rather than delete, any exact redundant local source material to a
   named recovery location, and report it;
8. replace repository metadata only after the new remote, bundle, overlay,
   permissions, and rollback path are verified.

Never reset, clean, stash, force-checkout, rewrite, or force-push the dirty
tree. Never hide unrelated work with a blanket ignore. If a safe in-place
migration cannot be proven, keep the live tree intact and leave the prepared
overlay beside it with the remaining ownership gap reported; do not improvise
destructive cleanup.

## Invariants

Preserve all of these throughout the work:

- visible names `DDX | Testing` and `DDX | AiP-Race`;
- UDP ports 8305 and 8306 and their existing firewall rules;
- each server's current map, password behavior, RCON credentials, vote policy,
  client limits, registration, SQLite state, logs, FIFO, and dashboard ID;
- DDX owner/admin/moderator/helper hierarchy and `sv_test_cmds 0`;
- `aip`, grenade bounces, sudo spectator movement, target `super`/`unsuper`, player handoffs, map archive
  browsing, owner-managed search collections, random choices, cache bounds, and single-writer extraction;
- AiP-Race's empty vote menu, disabled `/map`, fixed map, and lack of archive
  dependencies;
- independent deployment binaries and mutable runtime paths;
- the single historical archive and shared read-only map collection;
- KOG Lab, Multi TAS, and every unrelated service, file, listener, firewall
  rule, dashboard entry, backup input, and release;
- all unrelated tracked, staged, unstaged, ignored, and untracked work.

No service may execute a mutable source tree. No deployment may point at
another deployment's config, binary, secret, state, FIFO, logs, or cache.

## Work phases

Only one phase is active at a time. Keep a local task status with the current
phase, exact source revisions, last verified result, next action, accepted
decisions, open findings, evidence paths, and rollback artifacts. It is an
operational checkpoint, not a transcript. Store noisy logs and review ledgers
under an ignored task artifact directory; never commit them.

### Phase 1: establish the immutable baseline

Record production unit state, PID, restart count, start timestamp, UDP listener
ownership, executable hash, configured identity, current map, player count, and
dashboard target for all four DDNet services. Record firewall and recovery
state. Capture exact Git state for all four repositories and any worktrees.

Exercise the current legacy map enough to prove which teleports work and which
extra tiles do not. Prefer a repeatable map fixture or server integration test
over manual recollection. Do not use client-visible behavior as the only source
of tile semantics; reconcile it with the recovered primary source.

Acceptance:

- every baseline fact has a re-runnable command or artifact;
- no file or service changed;
- the intended source and deployment bases are explicit;
- rollback copies and migration snapshots have exact identities.

### Phase 2: freeze the capability and compatibility contracts

Inventory every DDX delta against pinned DDNet 19.9 from the patch stack,
registrations, config variables, tests, deployment configs, and runtime. Update
the README capability list only from that evidence. Create a compact feature
matrix with feature owner, default, server selection, persisted state,
authority, lifecycle, tests, and deployment consumers if the README cannot
carry those details clearly.

Inventory every legacy tile and tele path. Classify it as accepted standard
behavior, accepted legacy teleport compatibility, necessary old race primitive,
deferred research, or dead/provisional implementation. Require exact source and
map evidence for the first three classes.

Acceptance:

- every executable compatibility path has one class and one owner;
- no accepted DDX command is confused with an old entity tile of a similar
  name;
- modern DDNet behavior is the default and reference contract;
- documentation makes unsupported historical tiles unmistakable.

### Phase 3: design the smallest clean implementation

Compare at least these approaches before editing:

1. trim the current mixed compatibility module in place;
2. split legacy teleport decoding and map-profile selection from character
   behavior;
3. convert legacy maps ahead of runtime and use only modern DDNet layers.

Select the smallest approach that preserves exact old-map teleport semantics,
keeps modern behavior untouched, has deterministic lifecycle ownership, and
does not make the archive or a converter a runtime prerequisite. The expected
direction is a narrow server-side legacy-teleport module with immutable
map-load profiles; reject it if source or measured behavior disproves it.

Define before implementation:

- profile identity and selector validation;
- map-load, reload, failure, and unload transitions;
- destination indexing and random-selection semantics;
- character entry/exit and anti-loop state;
- hook, velocity, weapon, super, checkpoint, team, death, reconnect, and map
  change behavior;
- malformed, missing-output, single-tile, duplicate, conflicting, and unknown
  cases;
- logging rate and contents;
- hot-path allocation and lookup budget;
- rollback boundary.

Acceptance: the design has one state owner, one-way data flow, observable
outcomes, explicit failure behavior, and no timer-driven or global-config
coordination.

### Phase 4: refactor the authoritative patch stack

Reproduce the current defects first. Edit the authored patch stack through the
repository's supported patch-development workflow. Keep patches cohesive and
ordered. Split mixed patches when that makes ownership, review, or future
maintenance materially clearer; preserve history without rebasing or amending
published commits.

Remove dead and unaccepted entity-tile handlers, per-character fields,
configuration, branches, helper tables, lifecycle hooks, snapshots, and tests.
Do not "fix" the collision admission path for the deferred IDs as a side effect.
Keep historical definitions in passive research documents where useful. Do not
leave commented code, compatibility aliases, placeholder TODOs, duplicate
selectors, or a generic abstraction for hypothetical future tiles.

Implement the accepted tele path at the owning collision/map-load and
character-transition layers. Precompute destinations once. Keep tick handling
bounded, allocation-free, and direct. Derive presentation and logs from the
effective profile; never maintain duplicate booleans for the same state.

Preserve or improve behavior with fewer concepts and less executable code.
Fewer lines are valuable only when control flow, ownership, error handling, and
performance remain clear. Do not compress readable code into clever code.

Acceptance:

- the patch stack applies from a clean pinned upstream archive;
- generated source contains no stale rejected path;
- exact-map auto-selection cannot leak across map changes;
- every accepted DDX feature still compiles and has an owning test;
- the final source diff has no unrelated formatting or cleanup.

### Phase 5: prove behavior and performance

Add the smallest tests that prove contracts rather than implementation trivia.
At minimum cover:

- selector bounds and fail-closed behavior;
- exact size plus full SHA-256 profile matching;
- mismatched size, hash, name, and raw-ID lookalikes;
- legacy map → modern map → legacy map state isolation;
- paired teleport destination indexing and entry/output polarity;
- normal, evil, checkpoint, velocity, weapons, own hook, other hooks, super,
  and anti-loop behavior;
- missing output, one-tile combined teleporter, several outputs, duplicate
  outputs, malformed layers, maximum dimensions, and reload failure;
- character death, respawn, team change, reconnect, map change, shutdown, and
  interrupted load;
- modern DDRace maps and all ordinary DDNet tile validators;
- accepted DDX commands, owner authority, sudo spectator movement, map archive, cache, handoff, AiP, and
  grenade behavior;
- sanitized deployment manifests and scripts.

Use unit tests for pure decoding and state transitions, repository-native
server tests for ownership, and a real server/client or protocol-level path for
the accepted map behavior. Run map-reload sequences on an isolated test server,
never by changing a production server's configured or active map. A direct
FIFO command is not a substitute for a gameplay integration path.

Measure map-load cost, destination-index memory, and per-tick character cost
against the current accepted build on representative modern and legacy maps.
No regression may be accepted on the ordinary map hot path without a measured,
documented reason.

Run narrow tests first, then the complete affected test suite, formatting,
lint/static checks provided by the repository, a clean patch application, the
full server build, and all server tests. Retain full failure logs locally and
report only actionable diagnostics.

Acceptance: current evidence proves the retained teleports, unchanged modern
behavior, accepted DDX features, lifecycle isolation, malformed-input failure,
and performance bounds.

### Phase 6: reconcile source and deployment repositories

Make `/srv/ddx` the sole source authority. Make each deployment overlay pin the
verified DDX commit and describe its enabled features. Synchronize README,
feature manifest, revision pin, sanitized config, storage config, binary/map
manifest, service template, verification script, recovery inventory, and
dashboard contract.

For DDX Testing, follow the migration safety sequence above. Track only the
small deployment overlay. Keep the archive, maps, live binary, skin, secrets,
state, logs, FIFO, and runtime data outside Git with exact ignore and recovery
rules. Preserve the historical archive as a single copy.

For AiP-Race, keep the exact map identity:

- filename `AiP-Race.map`;
- size `421611`;
- SHA-256
  `04b91f0f6dc23d786daa83568e3545f5a9c1bec06dcf6d93625ed396b061895c`.

Do not change its fixed-map or no-vote contract. Update its binary manifest and
DDX revision pin only after the new source build is final.

Configure the verified LgcY-v2 Git identity. Inspect exact staged paths and the
staged diff for each cohesive commit. Commit with the repository's concise
lower-case convention. Push normally to canonical branches. Do not amend the
published history, force-push, blanket-stage, or include build output, runtime
data, research downloads, or secrets.

Acceptance:

- all canonical repositories are clean except explicitly preserved unrelated
  work;
- every published revision is reachable from its canonical branch;
- deployment pins, manifests, recovery policy, and dashboard catalog agree;
- secret and large-file scans are clean;
- no unique local work was lost or silently absorbed.

### Phase 7: build, stage, and deploy safely

Create immutable rollback copies and record current binary hashes. Build once
from the final DDX source and run the complete gate again. Install the verified
binary atomically into each DDX deployment's private executable path.

Do not restart KOG Lab, Multi TAS, or any unrelated service. Deploy one DDX
server at a time:

1. recheck all baseline services, listeners, and restart counters;
2. verify the target's port is owned only by its current PID;
3. install only the target's private binary;
4. restart only that target through its supported helper;
5. verify readiness, identity, map, port, auth behavior, voting policy, logs,
   FIFO, dashboard data, and restart count;
6. exercise the relevant teleport acceptance route;
7. observe a bounded soak period and compare non-target services with the
   baseline;
8. proceed to the second DDX target only if the first is healthy.

Rollback immediately to the recorded prior binary if startup, identity,
accepted gameplay, auth, voting, socket ownership, dashboard control, or the
soak gate fails. Preserve failure evidence. Do not repeatedly restart an
unchanged failing build.

Update and deploy the dashboard only if an authoritative catalog, recovery,
manifest, or revision reference must change. Use its supported release process;
never edit `/opt/vps-dashboard` release contents. A source-only DDX change does
not justify unrelated dashboard churn.

Acceptance:

- both DDX services run the intended identical build hash where configured;
- DDX Testing is `DDX | Testing` on UDP 8305 with its existing active map and
  archive browser;
- AiP-Race is `DDX | AiP-Race` on UDP 8306 with `AiP-Race`, zero votes, and no
  archive initialization;
- both dashboard panels, player data, logs, console, and controls target only
  their own service;
- KOG Lab and Multi TAS retain their original PID, start timestamp, port,
  configuration, files, and healthy state unless an external event is proved;
- unexpected restarts are zero.

### Phase 8: recovery and final review

Validate the supported recovery inventory after repository and manifest
changes. It must include each startup asset required by policy and exclude
secrets and mutable runtime data. If the deployed binary or recovery contract
changed, run one supported recovery backup and verify the local and offsite
point through normal tooling. Report normal retention deletion explicitly.

Verify a restore plan without overwriting production: repository revisions,
binary and map hashes, configs, storage, skin, service unit, permissions,
ownership, ACLs, firewall, dashboard catalog, and startup validation must lead
to the same server identity and behavior.

Run two final passes after all fixes:

1. correctness and ownership;
2. failure handling, security, recovery, scope, performance, and simplicity.

Any finding reopens its owning phase and the affected integration checks.

## Independent adversarial reviews

Use `prompt_standard_v2.md` literally: **100** is the first complete version
that satisfies the contract and **120** is the saturated version. These are
quality states, not a demand for 100–120 repetitive executions. Do not rerun an
unchanged test, invent findings, split one observation, or churn correct code to
meet a count.

Each review below must independently establish its 100 baseline, challenge the
result toward 120 with materially different hypotheses, record findings and
evidence in the local review ledger, and close only after two independent
passes find no unambiguous in-scope improvement. A change admitted by one
review reopens every affected review.

### Scope and preservation

Argue that the work touched an unauthorized service, dirty hunk, runtime file,
archive, map, credential, listener, firewall rule, dashboard entry, or
repository. Compare exact before/after inventories and hashes. Treat unexplained
change as a defect.

### Upstream DDNet regression

Assume every compatibility hook can alter modern DDRace behavior. Attack tile
ID collisions, layer validation, controller behavior, tune zones, teams,
checkpoints, stoppers, switches, tele weapons, map reload, and stock-client
prediction. Require modern maps to remain the control group.

### Historical-source fidelity

Assume memory and map appearance are wrong. Trace each retained legacy
semantic to pinned primary source, exact map bytes, and an observed route. Flag
unavailable or contradictory evidence instead of filling gaps by analogy.

### Decoder and profile correctness

Attack full-hash matching, size matching, selector bounds, integer ranges,
signedness, tile polarity, destination numbering, duplicate destinations,
layer presence, malformed data, and profile reset. Try to make one map inherit
another map's state.

### Teleport gameplay semantics

Attack velocity, weapons, hook ownership, evil behavior, super exceptions,
checkpoint ordering, team state, entry edges, repeated ticks, spawn overlap,
single-tile pairs, random destination selection, and immediate loops. Require
observable end-to-end evidence.

### Lifecycle and state ownership

Search for competing writers, global config mutation, stale cached maps,
character state surviving death or reconnect, map-load partial state, shutdown
leaks, semantic queues, timers, and hidden booleans. Every state must have one
owner and explicit terminal transitions.

### Code legibility and deletion

Review as a maintainer unfamiliar with the patch. Remove dead code, repeated
lookups, duplicate conditions, unnecessary state, vague names, broad helpers,
speculative abstractions, defensive code without a failure contract, and
comments that restate syntax. Prefer reuse of existing DDNet primitives when
semantics are actually identical. Optimize for fewer concepts and direct
control flow, not minimum characters.

### Patch-stack quality

Apply every patch from a clean pinned base. Challenge patch order, subject,
scope, generated diffs, context fragility, dependency leakage, test placement,
and rebuild reproducibility. Verify the build identifies the intended upstream
and DDX revisions.

### Performance and resource bounds

Measure rather than infer. Attack map-load scans, allocations, destination
storage, per-character tick work, random selection, logging, malformed-map
amplification, repeated reloads, and archive interaction. Compare representative
modern, legacy, small, and large maps.

### Security and untrusted input

Treat maps, config selectors, FIFO input, RCON commands, paths, archive
metadata, network clients, and dashboard requests as untrusted at their
boundaries. Attack auth rank, path traversal, resource exhaustion, log
injection, secret exposure, client-string trust, and password-admission reuse.

### Test validity

Try to make every test pass while the behavior is broken. Reject tests that
only restate lookup tables, inspect private implementation, use the wrong
binary, skip the real map path, or share state accidentally. Add only the
smallest proof for a credible regression.

### Build and reproducibility

Start from the published repositories and declared assets. Challenge missing
submodules, unpinned tools, environment dependence, stale generated source,
revision stamping, parallel builds, interrupted builds, and binary manifest
updates. Recovery must not depend on a developer's dirty tree.

### Deployment isolation and rollback

Assume target selection can hit the wrong service. Attack ambiguous defaults,
shared binaries, PID reuse, port races, partial atomic installs, failed starts,
restart loops, stale systemd state, and rollback mismatch. Every operation must
resolve one explicit target and verify the result.

### Repository and secret hygiene

Inspect all staged content, objects introduced by commits, ignore rules, large
files, remotes, branch ancestry, authorship, and generated artifacts. Search
for secrets without printing them. Prove no unrelated local change vanished,
moved into history, or became hidden.

### Deployment-overlay consistency

Compare revision pins, binary/map manifests, sanitized configs, storage,
service templates, verification scripts, dashboard entries, log rotation,
trash rules, backup inventory, exclusions, and recovery policy. One mismatch
means the deployment contract is not complete.

### Recovery

Assume the VPS and Git checkout are lost. Prove the supported local and offsite
point can restore the intended source revisions and startup assets without
including credentials or mutable player state. Verify artifact identity, not
only backup command success.

### Observability and diagnosis

Make selector rejection, profile choice, unsupported encodings, map-load
failure, teleport-index failure, startup failure, and rollback diagnosable
without noisy per-tick logs or private data. Logs must identify the owning map
and decision once.

### Documentation accuracy

Compare every feature, command, default, selector, path, hash, example, and
limitation with source and deployed behavior. Remove history narration,
unsupported claims, inflated language, duplicated explanation, and generic
prose. A new operator must know which features exist, which deployment enables
them, and what remains deferred.

### Future-feature containment

Try to smuggle a client, editor, tile-art, protocol, generic mod framework, or
hypothetical feature API into the cleanup. Delete it. Confirm that the narrow
teleport design does not prevent a later feature from receiving its own full
contract, but do not build that future contract now.

### Simplicity and proportion

Argue that the same verified outcome needs fewer files, states, flags,
branches, wrappers, tests, or operational steps. Keep a construct only when it
owns a real contract or measured constraint. Reject both premature abstraction
and compressed cleverness.

## Final production checks

Do not report completion until current evidence confirms:

- the source patch stack applies cleanly and the full server build and tests
  pass;
- published Git, local source, deployment pins, manifests, and deployed
  binaries agree;
- accepted DDX features match the README inventory;
- the verified legacy teleports work after a fresh start and after a
  legacy → modern → legacy reload sequence on an isolated test
  server;
- unsupported historical cheat tiles are neither claimed nor active runtime
  features;
- standard DDNet/DDRace maps retain their behavior;
- DDX Testing and AiP-Race retain their names, ports, maps, passwords, auth,
  votes, state, logs, FIFO, dashboard isolation, and expected restart counts;
- AiP-Race's exact map manifest verifies and its vote menu remains empty;
- archive/catalog initialization occurs only on DDX Testing;
- KOG Lab, Multi TAS, and unrelated services and files match the baseline;
- no archive or large map collection was duplicated;
- canonical repositories and recovery points contain no secrets, binaries,
  runtime data, or unrelated work;
- no history was rewritten and no force-push occurred;
- the supported recovery point contains every intended startup asset and none
  of the excluded credentials or mutable state;
- both final review passes and every reopened gate are closed at saturation.

## Handoff

Report only:

- canonical repository URLs and pushed commits;
- the final DDX and upstream revision identities;
- changed authored paths by repository;
- deployed binary hash and each target unit, PID, port, map, restart count, and
  dashboard state;
- repository-migration and rollback artifact locations;
- backup identity and verified contents/exclusions;
- test, integration, performance, security, repository, and recovery checks;
- any material file intentionally moved to recovery and how to restore it;
- any genuinely unverified item or residual risk.

Do not call the result perfect or claim an unobserved check.
