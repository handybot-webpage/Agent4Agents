# Pending decisions (append-only)

Non-blocking ambiguities the agent surfaced but did not block on. Reviewed
asynchronously, not at PR time. Entries are never deleted; resolved
decisions get a Resolution column entry.

| Timestamp | Charter | Question | Default in use | Resolution |
|---|---|---|---|---|
| 2026-05-06 | compact-bind | Should the bridge protocol formalize a "framework-implicit paths" set (`tasks/<id>.evidence.md`, `tasks/silent-decisions-log.md`, `tasks/pending-decisions.md`, `agent-context/30-active-charter.md`) that every Tier 1+ task may write to without declaring them in `## In-scope`? Surfaced because `compact-bind` flagged disjoint roots when these were declared. | Charters omit framework-implicit paths from `## In-scope`; protocol writes are allowed by convention. | pending — future Tier 2 ADR on `agent-context/05-bridge-protocol.md` |
| 2026-05-09 | readme | `bin/compact-bind` falsely flags single-root-file Tier 1 charters (e.g. scope is just `README.md`) as disjoint-roots, because their common parent is `.`. Disjoint should require *multiple distinct dirs* AND root common parent, not just root common parent. | Skip running compact-bind on charters whose scope is a single root-level file; manually verify scope. | pending — future Tier 1 fix in `bin/compact-bind` (`common_parent`/disjoint logic) plus added test case |
