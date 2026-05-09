# Charter — readme

**Tier:** 1
**Goal:** Write an extremely high-quality `README.md` — the project's front door. Convey what Project Compact is, why it exists, how to start, what it composes with (gstack), what's honest vs hype, and how to contribute. Link out to `ARCHITECTURE.md` for depth instead of duplicating.

## In-scope
- `README.md`

## Out-of-scope
- `ARCHITECTURE.md` (separate doc; this README links to it)
- `AGENTS.md` (separate doc; agent-facing read order)
- `agent-context/0*-*.md, 1*-*.md, 2*-*.md` (frozen prefix)
- `docs/adr/**` (any change is its own Tier 2)
- `bin/**` (no code changes)
- `.github/workflows/**` (governance)
- `.gitignore`

## Linked ADRs
- ADR-0001 — Markdown is the data layer (README is markdown, naturally)
- ADR-0004 — Integrate gstack as the workflow engine (README explains the integration to readers)

## Linked MODULE.md
- (none — `README.md` is a root-level cross-cutting doc)

## Acceptance evidence
- **Content sections:** elevator pitch, problem, solution, quick start (new + existing), architecture summary, demonstrated working (linking PR #1), Compact↔gstack augmentation summary, performance & honesty, status & roadmap, FAQ, contributing, license note, references.
- **Honest claims:** efficiency range stated as 20–100× compounded with the high-end conditions. No "1000×" headline. Concession: explicit list of what the framework does not solve.
- **Length:** ≤500 lines, ≥250 lines (substantial but readable).
- **Links:** every internal link points to a file that exists in this repo at HEAD.
- **Renders cleanly** as GitHub-flavored markdown.

## Charter-Approved-By
self-approved (Tier 1, single-developer)

---

## Note on compact-bind for this charter
The single-entry root-level scope (`README.md`) would currently be misclassified
by `bin/compact-bind` as disjoint-roots-Tier-1 because its common parent is `.`.
This is a known edge case, filed in `tasks/pending-decisions.md` for a future
Tier 1 fix. For this charter, the freeze scope is manually `.` (repo root);
the discipline boundary is "only `README.md` may be edited".
