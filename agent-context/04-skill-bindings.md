# 04 — Skill bindings (gstack ↔ Compact)

Frozen. Maps every tier in `02-tier-rubric.md` to the gstack skills that must
or may run. gstack supplies the workflow engine; Compact supplies the
substrate (cache, ADRs, tiers, charters, evidence).

## Tier 0 — Patch
- **Required:** none. Tier 0 changes are too small to ceremony.
- **Optional:** `/review` (light pass) before commit if you're unsure.
- **Forbidden:** `/ship` directly — Tier 0 still goes through normal commit,
  not gstack's release flow.

## Tier 1 — Feature
- **Required at task start:** `/freeze` — bind to the deepest common parent
  of the charter's `in-scope` globs (see `05-bridge-protocol.md`).
- **Required at task end:** `/review` (full), then `/qa` if any UI is touched,
  then evidence collection (see `05-bridge-protocol.md`).
- **Required to merge:** `/ship` only after `evidence.md` is populated and
  `silent-decisions-log.md` reflects all defaults taken this task.
- **Recommended:** `/codex` for cross-model second opinion before `/ship`.
- **Forbidden:** `/autoplan`, `/office-hours` — Tier 1 is too small for full
  planning ceremony.

## Tier 2 — Architectural
- **Required at task start:** `/office-hours` (surface assumptions),
  `/autoplan` (CEO + design + eng review), then `/freeze` per charter.
- **Required during build:** `/investigate` if root cause is unclear (3-fix
  limit prevents loops).
- **Required at task end:** `/review` (full), `/codex` (mandatory cross-model
  review), `/qa` if UI touched, `/cso` if anything on the irreversibility
  list around auth/billing/secrets is touched.
- **Required to merge:** `/ship`, then `/land-and-deploy`, then
  `/document-release` to update project docs.
- **Required after merge:** `/retro` within 24h to extract learnings; any
  recurring pattern (≥3 occurrences in `~/.gstack/projects/<slug>/learnings.jsonl`)
  is promoted to a new ADR (see `05-bridge-protocol.md`).
- **Approval:** `Charter-Approved-By:` trailer on charter file by a
  non-agent identity.

## Cross-tier rules
- `/freeze` is **always** invoked at the start of any Tier 1 or Tier 2 task,
  bound to the charter scope. The agent does not edit outside the freeze
  boundary; gstack's PreToolUse hook will block attempts.
- `/learn` writes are session-scoped. To survive across sessions and become
  governance, learnings must be promoted to an ADR (see `05-bridge-protocol.md`).
- `/codex` is the adversarial reviewer. Compact does not run a separate
  adversarial subagent — `/codex` (different vendor, different model) is
  strictly more independent.

## Skill replacements (gstack already does what Compact deferred)
- Adversarial review → `/codex`. (Compact's planned subagent is dropped.)
- Scope hook → `/freeze`. (Compact's planned PreToolUse hook is dropped.)
- QA / evidence collection → `/qa`. (Compact's evidence parser becomes a
  thin link to gstack's QA artifacts.)
- Multi-perspective plan review → `/autoplan` + `/plan-eng-review` +
  `/plan-design-review` + `/plan-ceo-review`. (Compact's tier rubric
  decides *whether* to invoke them; gstack provides the *how*.)

## What Compact still owns
- Append-only ADRs (`docs/adr/`) and the cache-aligned context prefix.
  These are the load-bearing primitives gstack does not provide.
- The tier rubric. gstack runs the same skills regardless of task size;
  Compact decides which skills are required for which tier.
- The charter as the source of truth for `/freeze` boundaries and
  in-scope/out-of-scope declarations.
- Silence-as-proceed protocol. gstack uses traditional clarifying questions.
