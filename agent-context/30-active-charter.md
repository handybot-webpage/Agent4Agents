# 30 — Active charter

**Source:** [`tasks/compact-bind.charter.md`](../tasks/compact-bind.charter.md)

---

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
- ADR-0001 — Markdown is the data layer
- ADR-0004 — Integrate gstack as the workflow engine

## Acceptance evidence
- **Tests:** ≥4 charter shapes exercised (literal, wildcard, recursive, disjoint).
- **Commands:** `bin/compact-bind` against the active charter exits 0 with `bin`.
- **Edge cases:** disjoint-roots returns exit 1 for Tier 1, exit 0 with `.` for Tier 2.

## Charter-Approved-By
self-approved (Tier 1)

---

## Charter addendum (2026-05-06) — corrected in-scope

Original `## In-scope` listed framework-implicit paths (evidence,
silent-decisions log, active charter) which produced disjoint roots when
run through `bin/compact-bind`. This addendum supersedes the original
in-scope; framework-implicit paths are accessed per protocol.

## In-scope
- `bin/compact-bind`
