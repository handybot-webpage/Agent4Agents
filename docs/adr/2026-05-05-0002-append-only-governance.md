# ADR 0002 — Append-only governance, no history rewrites

- **Status:** Accepted
- **Date:** 2026-05-05
- **Supersedes:** —
- **Superseded by:** —

## Context
Two failure modes dominate agent work on long-lived projects:

1. **Re-litigation.** Agents repeatedly revisit settled architectural questions
   because they cannot tell which decisions are firm.
2. **Cache invalidation.** Claude prompt caching depends on byte-stable file
   prefixes. Any edit to a cached file invalidates everything behind it,
   re-paying the full prefix on the next turn.

A single mechanism addresses both: never edit historical records. Only append.

## Decision
The following are append-only:

- ADR files (`docs/adr/*.md`) — once `Status: Accepted`, the body is immutable.
  To change the decision, write a new ADR with `Supersedes: <old>` and update
  the old ADR's `Superseded by:` field. The old ADR's body remains intact as
  history.
- ADR index (`agent-context/10-adr-index.md`) — append rows, never edit.
- Module index (`agent-context/20-module-index.md`) — append rows, never edit.
- Decision logs (`tasks/silent-decisions-log.md`, `tasks/pending-decisions.md`)
  — append entries, never delete.
- Charters (`tasks/<id>.charter.md`) — once approved, addenda go below the
  original; the original body is immutable.

## Consequences
- ADR index will grow without bound. Mitigation: time-windowed index (last
  90 days inline; older moves to `docs/adr/archive/` with a single index
  pointer to the archive).
- Filename collisions on ADRs. Mitigation: timestamp prefix
  (`YYYY-MM-DD-NNNN-slug.md`) so two PRs racing for the same number do not
  conflict on the filename.
- Reviewers must read the supersedence chain to understand current state.
  Mitigation: `compact-check` exposes a "show current decisions" view that
  walks the chain.

## Why this is non-negotiable
Without append-only, the cache architecture collapses (one edit invalidates
everything) and the re-litigation problem returns. Append-only is the
load-bearing assumption of the entire system.
