# ADR 0004 — Integrate gstack as the workflow engine

- **Status:** Accepted
- **Date:** 2026-05-05
- **Supersedes:** —
- **Superseded by:** —

## Context
Project Compact provides a governance substrate (cache-aligned context
prefix, append-only ADRs, tier rubric, charters, silence-as-proceed). It
deliberately deferred several capabilities to a v2.1 phase: adversarial
review, scope-enforcement hooks, real QA, multi-perspective plan review,
release flow.

gstack (Garry Tan's open-source Claude Code skill set, ~71K stars,
~46 skills) ships exactly those capabilities, battle-tested:
- `/freeze` — PreToolUse hook that blocks edits outside an allowed dir
- `/codex` — calls OpenAI for cross-model adversarial review
- `/qa` — real Chromium browser testing with regression test generation
- `/autoplan`, `/plan-{ceo,eng,design,devex}-review` — multi-perspective
  plan review with auto-decisions
- `/ship`, `/land-and-deploy`, `/document-release` — full release flow
- `/cso` — security review (OWASP + STRIDE)
- `/learn`, `/retro` — session memory and reflection

Building these from scratch in Compact would duplicate work and miss the
maturity of gstack's adoption. Compact's load-bearing primitives — cache
alignment, append-only ADRs, tier rubric — are precisely what gstack
does NOT provide.

## Decision
Compact and gstack are integrated, not merged. The integration model:

- gstack is installed globally at `~/.claude/skills/gstack/` and provides
  all 46 skills as Claude Code slash commands.
- Compact provides the data layer in this repository:
  `agent-context/`, `docs/adr/`, `tasks/`, `<module>/MODULE.md`.
- Two new frozen context files — `agent-context/04-skill-bindings.md`
  and `agent-context/05-bridge-protocol.md` — wire the two together:
  - `04-` maps each tier in `02-tier-rubric.md` to required and
    optional gstack skills.
  - `05-` specifies the data handshakes (charter→/freeze,
    /qa→evidence.md, /codex→ADR, /learn→ADR promotion).

The following items in Compact's deferred backlog are **dropped** because
gstack already implements them better:
- Adversarial review subagent → `/codex` (different vendor = stronger).
- PreToolUse scope hook → `/freeze` (already production-tested).
- Evidence parser as primary mechanism → thin layer on top of gstack's
  `/qa` and `/review` artifacts.
- Multi-perspective plan review → `/autoplan` and the `/plan-*-review`
  skill family.

The following remain **uniquely Compact's responsibility**:
- Cache-aligned context layout (`agent-context/00-` through `30-`).
  gstack does not optimize for prompt-cache stability the same way.
- Append-only ADRs as immutable architectural memory. gstack's `/learn`
  is session-scoped; ADRs are decision-scoped law.
- Tier rubric (Tier 0 / 1 / 2) deciding which skills are required.
  gstack runs the same workflow regardless of task size.
- Silence-as-proceed protocol for reversible decisions. gstack uses
  traditional clarifying questions inside its plan-review skills.
- Charter as the source of truth for `/freeze` boundaries and
  in-scope/out-of-scope declarations.

## Consequences
- **Velocity:** Tier 1 and Tier 2 tasks immediately get gstack's full
  workflow (plan review, freeze enforcement, QA, codex, ship, retro)
  without Compact reimplementing any of it.
- **Discipline:** Compact's tier rubric and append-only ADRs prevent the
  decision-amnesia and ceremony-mismatch failure modes of vanilla gstack.
- **Cache cost:** the bridge adds ~140 lines to the cache-aligned prefix
  (files `04-` and `05-`). One-time invalidation on next agent run; then
  stable. Total prefix size remains comfortably under the
  ~150-instruction reliability cliff *per file* and ~500-line aggregate.
- **Vendor coupling:** Compact now depends on Claude Code (for skills) and
  on gstack (for skill content). Mitigation: the data layer
  (`docs/adr/`, `agent-context/00-` through `30-`, `tasks/`) is plain
  markdown that survives a switch of either dependency. Only the skill
  bindings file (`04-`) would need rewriting against a different skill
  set.
- **Update cadence:** gstack ships `/gstack-upgrade` for self-update.
  Bridge files `04-` and `05-` may need updating when gstack adds or
  renames skills. Each such update is a Tier 2 change with a new ADR.
- **Telemetry:** gstack's optional telemetry is OFF unless explicitly
  enabled. The bridge does not enable it.
- **Security boundary:** gstack's `/freeze` is a deny-default PreToolUse
  hook — strictly stronger than prose constraints. This closes Compact's
  largest enforcement gap from prior critique.

## Alternatives considered
- **Compact only.** Build adversarial review, hooks, QA, plan review from
  scratch. Rejected: months of work to reach gstack's maturity, with no
  community feedback loop.
- **gstack only.** Drop Compact's cache layout and ADRs. Rejected: gstack
  has no equivalent to append-only architectural memory; re-litigation
  and cache cost would dominate.
- **Fork gstack.** Modify skills to consume Compact files directly.
  Rejected: forks decay; bridge protocol via two new context files
  preserves both upstream tracks.
