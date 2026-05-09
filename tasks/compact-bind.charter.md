# Charter — compact-bind

**Tier:** 1
**Goal:** Auto-extract the active charter's deepest common parent directory, removing the manual step at task start before invoking `/freeze`.

## In-scope
- `bin/compact-bind`
- `tasks/compact-bind.evidence.md`
- `tasks/silent-decisions-log.md` (append-only, audit entries)
- `agent-context/30-active-charter.md` (cache tail, allowed to swap)

## Out-of-scope
- `agent-context/0*-*.md`, `1*-*.md`, `2*-*.md` (frozen prefix)
- `docs/adr/**` (any change is its own Tier 2)
- `bin/compact-check` (separate concern)
- `.github/workflows/**` (governance changes are Tier 2)
- `AGENTS.md`, `ARCHITECTURE.md`, `.gitignore`

## Linked ADRs
- ADR-0001 — Markdown is the data layer (charter parsing reads markdown directly)
- ADR-0004 — Integrate gstack as the workflow engine (this script implements the charter→/freeze handshake from `agent-context/05-bridge-protocol.md` §10.1)

## Linked MODULE.md
- (none — `bin/` is not yet a formal module; will create one if the directory grows beyond 3 scripts)

## Acceptance evidence
- **Tests:** at least 4 charter shapes exercised inline (literal file path, wildcard glob, recursive `**` glob, disjoint roots). compact-bind outputs the correct deepest common parent for each.
- **Commands:** `bin/compact-bind` invoked against the active charter exits 0 with output `bin`.
- **Edge cases:** disjoint-roots case returns exit 1 for Tier 1 (per bridge protocol §10.1) and exit 0 with `.` for Tier 2.

## Charter-Approved-By
self-approved (Tier 1 — single-developer, audit-logged in `tasks/silent-decisions-log.md`)

---

## Charter addendum (2026-05-06) — corrected in-scope

The original `## In-scope` listed framework-implicit paths (evidence file,
silent-decisions log, active charter) alongside the actual work artifact.
Running `bin/compact-bind` against it correctly flagged disjoint roots
(`bin`, `tasks`, `agent-context`) for a Tier 1 charter — the framework's
own tooling caught the design flaw.

Per the append-only-within-a-task rule, the original `## In-scope` is
preserved above as history. This addendum's `## In-scope` supersedes it.
Framework-implicit paths are accessed per protocol, not per charter
declaration. The question of formalizing this is filed under
`tasks/pending-decisions.md`.

## In-scope
- `bin/compact-bind`
