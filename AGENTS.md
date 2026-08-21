# execution standard

authority
- follow the explicit task, then the nearest repository instructions. preserve mode: research/review do not edit; planning does not implement; implementation does not authorize commit, push, merge, release, or deploy.
- when constraints conflict, prioritize correctness/safety, security/privacy/contracts, ownership/reliability, requested outcome, performance, simplicity, then convention.
- resolve uncertainty from repository evidence and authoritative sources. ask only for an unresolved product choice, required access, or irreversible external action; otherwise take the safest reversible path.
- use live source, tests, schemas, configuration, runtime evidence, and authoritative upstream documentation as evidence. reconcile conflicts; never guess what can be checked.

scope
- own the requested outcome, not a larger product. include only adjacent work required for correctness; report the rest.
- preserve unrelated tracked and untracked work; never overwrite, move, reformat, clean, or absorb it.
- before editing, inspect the smallest evidence set sufficient to prove behavior, ownership, contracts, and risk: applicable instructions, code, callers/callees, tests, configuration, side effects, generated-file boundaries, and useful history.

implementation
- non-trivial means production behavior, public contracts, persisted data, security, concurrency, performance, or cross-file behavior. use: understand -> compare viable approaches -> implement the smallest complete root-cause change -> verify -> inspect the final diff.
- change the owning layer to fix source defects; compensate at a boundary only when its contract requires it.
- apply `$dumb-robust-systems` to non-trivial stateful, asynchronous, concurrent, control, simulation, search, optimization, or reliability work.
- prefer deletion, direct ownership, existing primitives, and explicit contracts. add wrappers, flags, retries, timers, queues, abstractions, compatibility layers, or dependencies only for a necessary contract or measured constraint.
- make boundary units, origin, ordering, precision, encoding, ownership, and failure semantics explicit. preserve public contracts and persisted data; migrations require compatibility and defined failure, recovery, and rollback behavior.
- validate untrusted input, permissions, and authorization at boundaries; fail closed. never expose or commit secrets, credentials, or private data.
- verify external api and dependency behavior against official documentation or source; never invent api behavior.
- edit authoritative source, not generated, vendored, dependency, or build output, unless explicitly owned by the task or repository.
- update affected tests, contracts, schemas, and current documentation together. comments explain only non-obvious invariants, constraints, or tradeoffs.
- measure before optimizing; protect hot paths from unnecessary allocation, io, computation, copying, and synchronization.
- leave no dead/commented code, placeholder todos, duplicate logic/authority, blanket formatting, or unrelated cleanup.

verification
- reproduce defects first when practical. add the smallest behavior/contract test that catches the defect or regression; do not test implementation trivia.
- run the narrowest relevant checks first, then broader tests, type checks, lint, formatting, builds, and integration checks by risk. use repository-native commands.
- exercise the actual runtime/integration path when practical. verify resulting behavior/state, not only an exit code, elapsed time, resolved promise, or passing substitute.
- cover relevant normal, boundary, error, interruption, cancellation, stale, retry, and partial states.
- never weaken tests. investigate failures; never hide, blindly retry, or rerun unchanged work until it passes.
- use native quiet flags or capture noisy output. stream no successful build/test logs. on failure show the command, exit status, and smallest actionable diagnostics; retain the full log when available.
- never claim an unobserved check, path, or result. distinguish verified, inferred, and unverified conclusions.
- non-trivial completion requires current evidence, no known in-scope defect, and two distinct final passes: correctness/ownership; then failure/security/scope/performance/simplicity. repeat only for actionable findings; stop at saturation; state unverified gaps.

git
- follow task and repository delivery policy. do not initialize, commit, push, merge, rebase, amend, tag, release, or deploy without authorization.
- before editing or delivery, inspect branch, status, and diff. stage exact paths and inspect the staged diff; never blanket-stage or include unrelated files.
- never reset, clean, stash, discard, rewrite history, force-push, or alter unrelated work without explicit authorization.
- never commit secrets, local state, logs, archives, binaries, or generated output unless intentionally tracked.
- make cohesive, verified commits with one subject: `<type>: <lower-case imperative outcome>`. after the prefix use letters and spaces only. types: `feat`, `fix`, `refactor`, `perf`, `test`, `docs`, `build`, `ci`, `chore`, `release`, `revert`.
- write commits like private notes for one ddnet developer. keep the subject short and plain. add a body only when the change is substantial, using a few raw `-` bullets about code behavior.
- no scope, trailers, issue ids, emojis, hype, attribution, assistants, models, prompts, plans, generated work, tools, or polished release prose.

communication
- keep updates and final output minimal: outcome, changed paths, checks, unresolved risk. omit narration and raw successful command output.
