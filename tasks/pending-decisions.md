# Pending decisions (append-only)

Non-blocking ambiguities the agent surfaced but did not block on. Reviewed
asynchronously, not at PR time. Entries are never deleted; resolved
decisions get a Resolution column entry.

| Timestamp | Charter | Question | Default in use | Resolution |
|---|---|---|---|---|
| 2026-05-06 | compact-bind | Should the bridge protocol formalize a "framework-implicit paths" set (`tasks/<id>.evidence.md`, `tasks/silent-decisions-log.md`, `tasks/pending-decisions.md`, `agent-context/30-active-charter.md`) that every Tier 1+ task may write to without declaring them in `## In-scope`? Surfaced because `compact-bind` flagged disjoint roots when these were declared. | Charters omit framework-implicit paths from `## In-scope`; protocol writes are allowed by convention. | pending — future Tier 2 ADR on `agent-context/05-bridge-protocol.md` |
