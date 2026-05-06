# AGENTS.md — Agents4Agents

This project runs under **Project Compact** with **gstack** as the workflow
engine. Read the cache-aligned context in [`agent-context/`](./agent-context/)
**in numerical order** before doing any work. Files `00-` through `20-` are
frozen and form a stable prompt-cache prefix; do not edit them as part of
a task.

## Read order on every session
1. [`agent-context/00-system.md`](./agent-context/00-system.md) — operating loop
2. [`agent-context/01-constitution.md`](./agent-context/01-constitution.md) — invariants + irreversibility list
3. [`agent-context/02-tier-rubric.md`](./agent-context/02-tier-rubric.md) — Tier 0/1/2
4. [`agent-context/03-question-protocol.md`](./agent-context/03-question-protocol.md) — silence-as-proceed
5. [`agent-context/04-skill-bindings.md`](./agent-context/04-skill-bindings.md) — gstack skills required per tier
6. [`agent-context/05-bridge-protocol.md`](./agent-context/05-bridge-protocol.md) — Compact↔gstack handshakes
7. [`agent-context/10-adr-index.md`](./agent-context/10-adr-index.md) — accepted decisions
8. [`agent-context/20-module-index.md`](./agent-context/20-module-index.md) — modules
9. [`agent-context/30-active-charter.md`](./agent-context/30-active-charter.md) — current task

## Cold context (fetch on demand)
- [`docs/adr/`](./docs/adr/) — full ADR text
- `<module>/MODULE.md` — module contracts (only for modules you touch)

## gstack
This project uses gstack skills installed at `~/.claude/skills/gstack/`. Use
the `/browse` skill from gstack for all web browsing — never use
`mcp__claude-in-chrome__*` tools.

Available skills: `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`,
`/plan-design-review`, `/plan-devex-review`, `/design-consultation`,
`/design-shotgun`, `/design-html`, `/design-review`, `/devex-review`,
`/review`, `/ship`, `/land-and-deploy`, `/canary`, `/benchmark`, `/browse`,
`/connect-chrome`, `/qa`, `/qa-only`, `/setup-browser-cookies`,
`/setup-deploy`, `/setup-gbrain`, `/retro`, `/investigate`,
`/document-release`, `/codex`, `/cso`, `/autoplan`, `/careful`, `/freeze`,
`/guard`, `/unfreeze`, `/gstack-upgrade`, `/learn`, `/pair-agent`.

Detailed mapping of tier → required skills lives in
[`agent-context/04-skill-bindings.md`](./agent-context/04-skill-bindings.md).

## Skill routing (summary)
- **Tier 0:** no required skills.
- **Tier 1:** `/freeze` at start, `/review` + `/qa` (if UI) at end, `/ship`
  to merge. `/codex` recommended.
- **Tier 2:** `/office-hours` + `/autoplan` at start, `/freeze` per charter,
  `/review` + `/codex` + `/qa` + `/cso` (if security) at end, then `/ship`
  → `/land-and-deploy` → `/document-release` → `/retro`.

## Question protocol summary
- REVERSIBLE decisions: declare default + reasoning, append to
  [`tasks/silent-decisions-log.md`](./tasks/silent-decisions-log.md), proceed.
- IRREVERSIBLE decisions (irreversibility list in `01-constitution.md`):
  one multiple-choice blocking question per turn, then wait.
- If the answer is in the loaded context, do not ask — read and proceed.

## Build / test / lint
_(none yet — this scaffold is the initial state. Adding the first toolchain
choice is itself a Tier 1 change with a charter and ADR.)_
