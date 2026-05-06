# 02 — Tier rubric

Every charter declares a tier on its first line. Tier governs ceremony.

## Tier 0 — Patch
- Single file edit
- No behavior change (typo, comment, formatting, dead-code removal)
- No public API touched
- No ADR contradicted
- **Required artifacts:** none beyond the PR description
- **Approval:** self-approved

## Tier 1 — Feature
- Touches multiple files within ONE module
- Behavior change, but no architectural decision
- Linked to existing ADRs and MODULE.md (no new ADR)
- **Required artifacts:** `tasks/<id>.charter.md`, `tasks/<id>.evidence.md`
- **Approval:** self-approval with audit log entry in `silent-decisions-log.md`

## Tier 2 — Architectural
- Crosses module boundaries, OR
- Contradicts or supersedes an existing ADR, OR
- Adds a new public API, OR
- Hits anything on the irreversibility list
- **Required artifacts:** charter + evidence + new ADR (if architectural)
  + adversarial-review subagent report
- **Approval:** explicit human approval via `Charter-Approved-By:` trailer
  signed by a non-agent identity

## Tier mismatch
The diff's actual tier (computed from touched modules, contradicted ADRs,
irreversibility-list hits) MUST match the declared tier. Mismatch is a
required-check failure on the PR.

## Splitting
A change too large for Tier 2 is split into multiple PRs, each with its own
charter. Cross-PR splitting to evade tier classification is itself a
protocol violation.
