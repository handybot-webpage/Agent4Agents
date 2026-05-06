# Architecture — Project Compact (with gstack as workflow engine)

**Status:** scaffold complete; first task pending
**Last updated:** 2026-05-05
**Companion docs:** [`AGENTS.md`](./AGENTS.md), [`agent-context/`](./agent-context/), [`docs/adr/`](./docs/adr/)

---

## 1. Purpose

Project Compact is the governance substrate for multi-agent + human software
development. It exists to solve four documented failure modes in agentic
coding at scale:

1. **Bogus work.** Agents invent adjacent tasks ("while I'm here…"),
   producing changes the human never asked for.
2. **Whack-a-mole on decisions.** Agents re-litigate settled architectural
   questions because they cannot tell which decisions are firm.
3. **Decision fatigue.** Agents pepper humans with clarifying questions
   that should have been inferred or batched.
4. **Token + time waste at scale.** Each turn re-reads context, re-derives
   conventions, and re-discovers state — costs that compound across
   thousands of turns and dozens of contributors.

Compact is paired with **gstack** (Garry Tan's open-source Claude Code
skill set, ~46 skills, battle-tested at scale) as the workflow engine.
gstack supplies the *forms and rituals* of a high-functioning team
(specialist roles, plan review, real QA, ship discipline). Compact
supplies the *constitution and code of the building* (cache-aligned
context, append-only ADRs, tier rubric, charters).

## 2. Non-goals

- **Not a coding agent.** Compact does not generate code. It governs
  agents that do.
- **Not a replacement for gstack.** Compact deliberately defers to gstack
  for plan review, scope hooks, QA, and release flow.
- **Not a build system or CI tool.** It generates artifacts that CI
  consumes; it does not run pipelines.
- **Not vendor-neutral.** The data layer is portable Markdown, but the
  enforcement layer assumes Claude Code as primary harness (per ADR-0003)
  and gstack as primary skill set (per ADR-0004).
- **Not a knowledge graph.** ADRs and MODULE.md files are append-only
  Markdown, not a queryable database. Build a derived index if needed;
  do not change the source format.

## 3. Design constraints

These are load-bearing. Every architectural decision is justified by one
or more of them.

| Constraint | Why it matters |
|---|---|
| 100× compounded efficiency vs ungoverned agent work | The user-facing target. Drives cache discipline. |
| Stand the test of time | No vendor primitives that decay. Markdown survives tool changes. |
| Multi-agent + human collaboration | Multiple agents must see the same canonical state. Humans must approve the few decisions that warrant it. |
| Modular and nimble | Tier 0 work pays zero ceremony. Only Tier 2 pays full ceremony. |
| Prevent fake work | Out-of-scope edits are mechanically blocked, not just discouraged. |
| Prevent decision fatigue | Silence-as-proceed for reversibles; blocking only for irreversibles. |
| Cache prompt context | The single biggest token-savings lever (~30× alone). |

## 4. Architecture at a glance

```
┌──────────────────────────────────────────────────────────────────────┐
│                          AGENTS.md (entry)                           │
│           "Read agent-context/ in numerical order. Use gstack."      │
└────────────────────────────────┬─────────────────────────────────────┘
                                 ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  agent-context/ — frozen cache prefix                │
│                                                                       │
│  00-system   01-constitution   02-tier-rubric   03-question-protocol │
│  04-skill-bindings   05-bridge-protocol                              │
│  10-adr-index (append-only)   20-module-index (append-only)          │
│  30-active-charter (swaps per task — only cache-tail mutation)       │
└─────────┬───────────────────────────────────┬────────────────────────┘
          ▼                                   ▼
┌──────────────────────┐           ┌──────────────────────────────────┐
│ docs/adr/            │           │ tasks/                           │
│ append-only ADRs     │           │ <id>.charter.md                  │
│ supersedence chain   │           │ <id>.evidence.md                 │
│ "law" of the project │           │ silent-decisions-log.md          │
└──────────┬───────────┘           │ pending-decisions.md             │
           │                       └────────────┬─────────────────────┘
           │                                    ▼
           │                  ┌────────────────────────────────────────┐
           │                  │   ~/.claude/skills/gstack/             │
           │                  │   46 skills as slash commands          │
           │                  │   /freeze /codex /qa /autoplan /ship   │
           │                  │   /review /investigate /retro /learn   │
           │                  │   /cso /office-hours …                 │
           │                  └────────────────────────────────────────┘
           ▼
┌──────────────────────────────────────────────────────────────────────┐
│            <module>/MODULE.md  (cold context, fetched JIT)           │
│            owner · public API · invariants · linked ADRs             │
└──────────────────────────────────────────────────────────────────────┘
```

The diagram captures the core split:

- **Compact** owns the data layer (left side: ADRs, charters, indexes,
  modules) and the cache-aligned context prefix.
- **gstack** owns the workflow engine (right side: 46 skills as slash
  commands, installed globally).
- The bridge files `04-skill-bindings.md` and `05-bridge-protocol.md`
  wire them together: Compact's tier rubric decides *which* gstack
  skills run; gstack's skills decide *how* they run.

## 5. The three layers

### 5.1 Substrate (Compact)
Always-on, passive. Loaded into every agent session in numerical order
to form a stable, byte-cached prefix.

- `agent-context/00-system.md` — operating loop
- `agent-context/01-constitution.md` — invariants + irreversibility list
- `agent-context/02-tier-rubric.md` — Tier 0/1/2
- `agent-context/03-question-protocol.md` — silence-as-proceed
- `agent-context/04-skill-bindings.md` — tier→gstack skill mapping
- `agent-context/05-bridge-protocol.md` — handshakes
- `agent-context/10-adr-index.md` — append-only decision index
- `agent-context/20-module-index.md` — append-only module index
- `agent-context/30-active-charter.md` — only cache-tail mutation

### 5.2 Workflow engine (gstack)
On-demand, active. 46 skills invoked via slash commands.

- **Planning:** `/office-hours`, `/autoplan`, `/plan-{ceo,eng,design,devex}-review`
- **Building:** `/freeze`, `/guard`, `/careful`, `/investigate`
- **Verification:** `/review`, `/qa`, `/qa-only`, `/codex`, `/cso`
- **Release:** `/ship`, `/land-and-deploy`, `/canary`, `/document-release`
- **Reflection:** `/retro`, `/learn`
- **Coordination:** `/pair-agent`, `/browse`, `/scrape`

### 5.3 Governance layer (Compact)
Per-task, gated.

- **Charter** (`tasks/<id>.charter.md`) — declares tier, in-scope,
  out-of-scope, linked ADRs, acceptance evidence.
- **Evidence** (`tasks/<id>.evidence.md`) — populated before "done"
  by piping gstack's `/qa` and `/review` artifacts.
- **Silent decisions log** (`tasks/silent-decisions-log.md`) — append-only
  audit of every reversible default the agent took without asking.
- **Pending decisions** (`tasks/pending-decisions.md`) — append-only
  parking lot for non-blocking ambiguities, reviewed asynchronously.

## 6. Data layer

### 6.1 Append-only invariants
Per ADR-0002, the following are append-only — once written, the body
is immutable:

- `docs/adr/*.md` — supersedence chain via `Supersedes:` /
  `Superseded by:` fields
- `agent-context/10-adr-index.md` and `20-module-index.md` — append rows
- `tasks/silent-decisions-log.md`, `tasks/pending-decisions.md`
- `tasks/<id>.charter.md` once approved — addenda go below the original

This invariant is load-bearing for two reasons:

1. **Cache stability.** Edits invalidate the prompt cache from that
   point onward. Append-only keeps the prefix byte-stable across
   hundreds of turns.
2. **Re-litigation prevention.** A superseded ADR's body remains intact
   as history. The current state is computed by walking the
   supersedence chain, not by mutating files.

### 6.2 File naming
- **ADRs:** `YYYY-MM-DD-NNNN-slug.md`. Timestamp prefix prevents
  filename collisions when two PRs race for the same number.
- **Tasks:** `<id>.charter.md`, `<id>.evidence.md` where `<id>` is a
  short slug (e.g. `add-auth`, `migrate-db-2026-q2`).
- **Modules:** `<module>/MODULE.md` co-located with the module's code.

### 6.3 Cold vs hot context
| Loaded every session (hot) | Fetched on demand (cold) |
|---|---|
| `agent-context/00-` through `30-` | `docs/adr/*.md` (full ADR text) |
| `AGENTS.md` | `<module>/MODULE.md` |
| | `tasks/silent-decisions-log.md` |
| | `tasks/pending-decisions.md` |

The hot prefix is currently **~341 lines / ~14KB / ~3.5K tokens** —
well under any reliability cliff. The ADR index uses one line per ADR
to stay bounded; old ADRs (>90 days) move to `docs/adr/archive/` and
are removed from the hot index.

## 7. Cache architecture

The single biggest contributor to the 100× target.

### 7.1 Why prompt caching matters here
Claude's prompt cache:
- Returns ~10% of write cost on cache hits
- Has a 5-minute TTL within a session
- Requires byte-stable prefixes — any edit invalidates everything after it

For an agent doing 10 turns on a task, a 14KB prefix that caches across
turns means paying 14KB *once*, not 10×. That's a 9× saving on prefix
tokens alone, before any other optimization.

### 7.2 The cache-stability rules
1. **Frozen prefix.** Files `00-` through `20-` are not edited as part
   of any task. Edits are batched into dedicated PRs (Tier 2, with their
   own ADR).
2. **Append-only indexes.** New rows in `10-adr-index.md` and
   `20-module-index.md` go at the bottom; existing rows are immutable.
3. **Charter at the cache tail.** `30-active-charter.md` is the only
   file expected to swap per task. Switching tasks invalidates only
   that suffix (~20 lines).
4. **Charter is append-only within a task.** Mid-task scope additions
   become *addenda below* the original charter, not edits to it.
5. **Time-windowed ADR index.** Old ADRs leave the hot index to keep
   it bounded as the project ages.

### 7.3 The five common cache-killers
Each of these alone collapses the multiplier to <10×:
- Editing files in the cache prefix mid-session
- Sequential ADR numbering (filename merge conflicts)
- Preloading every `MODULE.md` (kills the budget)
- Lead agent doing implementation work (pollutes its own cache)
- Long-running sessions without a 5-min keepalive read

These are documented in `agent-context/00-system.md` as constraints on
agent behavior.

## 8. Workflow layer (gstack)

### 8.1 Skill categories
| Phase | Skills |
|---|---|
| **Think** | `/office-hours` |
| **Plan** | `/autoplan` orchestrates `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/plan-devex-review` |
| **Build** | `/freeze`, `/guard`, `/careful` (boundary enforcement); `/investigate` (root-cause debugging with 3-fix limit) |
| **Verify** | `/review` (staff-eng pass), `/codex` (cross-model independent review via OpenAI), `/qa` (real Chromium browser tests), `/qa-only` (bug reporting), `/cso` (OWASP+STRIDE security) |
| **Ship** | `/ship` (bump version, push, PR), `/land-and-deploy` (post-merge health), `/canary` (post-deploy monitoring), `/document-release` (auto-update docs) |
| **Reflect** | `/retro` (per-person learnings), `/learn` (memory management) |
| **Coordinate** | `/pair-agent` (multi-AI through one browser), `/browse` (Chromium control with anti-bot stealth) |

### 8.2 Tier → skill mapping (full table in `04-skill-bindings.md`)

| Tier | Required at start | Required at end | To merge |
|---|---|---|---|
| 0 | none | none | none |
| 1 | `/freeze` (charter scope) | `/review`, `/qa` (if UI) | `/ship` (after evidence) |
| 2 | `/office-hours`, `/autoplan`, `/freeze` | `/review`, `/codex`, `/qa`, `/cso` (if security) | `/ship` → `/land-and-deploy` → `/document-release`, then `/retro` within 24h |

## 9. Governance layer

### 9.1 Tier rubric
The charter's first line declares its tier. Tier governs ceremony.

- **Tier 0 — Patch:** single file, no behavior change. No charter.
- **Tier 1 — Feature:** one module, multiple files. Charter + evidence.
- **Tier 2 — Architectural:** cross-module or contradicts an ADR.
  Charter + evidence + new ADR + human approval.

Tier mismatch (declared tier doesn't match actual diff scope) is a
required-check failure on the PR — once the enforcement script lands.

### 9.2 Irreversibility list
Per `01-constitution.md`, these always require explicit human approval
regardless of how the agent classifies a decision:

- DB schema migrations
- Adding/removing/upgrading dependencies
- Breaking public API or exported interface changes
- Deletion of any file >50 lines
- Anything touching auth, authorization, billing, or secrets
- Edits to `agent-context/0*-*.md`, `1*-*.md`, `2*-*.md`
- Edits to accepted ADRs (except appending new ones)
- Edits to `.claude/`, `.github/workflows/`, hook scripts

### 9.3 Charter approval (Tier 2)
Per the bridge protocol's approval handshake:

1. Agent writes the charter, leaves `Charter-Approved-By:` blank.
2. Agent commits the charter.
3. **A non-agent identity** edits the charter to add the trailer and
   commits separately.
4. Agent verifies the trailer was added by a non-agent commit before
   proceeding past planning.

This prevents agents from self-authoring and self-approving their own
contracts.

### 9.4 ADR supersedence
Per ADR-0002, decisions are append-only. To change one:

1. Write a new ADR with `Supersedes: <old>` field.
2. Update the old ADR's `Superseded by:` field (the only allowed edit).
3. Append the new ADR to `agent-context/10-adr-index.md`.

The old ADR's body remains intact as history. Current state is
computed by walking the chain.

### 9.5 Silent-decisions audit
Every reversible default the agent took without asking is appended to
`tasks/silent-decisions-log.md` with:

- Timestamp
- Charter ID
- Default chosen
- Alternatives rejected (one-line tradeoffs)

PR templates link this file. Reviewers can skim entries since the last
PR. Without this, silence-as-proceed degrades over time as humans
habituate.

## 10. Bridge protocol

The four data handshakes between Compact and gstack, from
`agent-context/05-bridge-protocol.md`:

### 10.1 Charter → /freeze
At task start, the agent reads `30-active-charter.md`, computes the
deepest common parent of all in-scope globs, and invokes `/freeze`
with that directory. gstack's PreToolUse hook then physically blocks
Edit/Write outside that boundary for the rest of the session.

### 10.2 /qa → evidence.md
After `/qa`, gstack writes results under
`~/.gstack/projects/<slug>/qa/<timestamp>/`. The agent appends one row
per regression test to `evidence.md`'s `## Tests` table, links the
screenshot/recording paths in `## UI evidence`, and records the
captured commit SHA.

### 10.3 /codex → ADR or evidence.md
At end of Tier 2, `/codex` returns agree / disagree / adversarial-flag.
- **Agree:** record in `evidence.md` `## Notes`.
- **Disagree:** revise OR write an ADR documenting why we proceeded
  against codex's recommendation.
- **Adversarial-flag:** block `/ship`. Resolve or write a superseding ADR.

### 10.4 /learn → ADR promotion
During `/retro`, group `~/.gstack/projects/<slug>/learnings.jsonl`
entries by topic. Any topic with **≥3 distinct entries** is an ADR
candidate: the pattern is recurring enough to deserve durable
governance. Write the ADR, append to the index, prune the related
learnings.

ADRs supersede learnings. The reverse never holds.

## 11. Augmentation matrix — what each layer adds to the other

This is the core "complementarity" view. Compact alone or gstack alone
each leaves real gaps. The combined system closes them.

### 11.1 What gstack gains from Compact

| Compact contribution | What gstack lacked |
|---|---|
| **Cache-aligned `agent-context/` prefix** | gstack skills are loaded on-invoke; no notion of cache-stable per-session context. Compact's prefix gives every gstack skill a cached substrate to reason against. |
| **Append-only ADRs as immutable architectural memory** | gstack's `/learn` is session-scoped pattern memory, not durable governance. ADRs survive tool changes, model changes, and team turnover. |
| **Tier rubric (Tier 0 / 1 / 2)** | gstack runs the same skill sequence regardless of task size. Compact decides which skills are required, eliminating ceremony on small work and enforcing it on architectural work. |
| **Silence-as-proceed for reversibles** | gstack's plan-review skills use traditional clarifying questions, generating decision fatigue. Compact's protocol cuts the back-and-forth. |
| **Charter as scope source of truth** | gstack's `/freeze` requires a manually-supplied directory. Compact's charter computes that directory deterministically from declared in-scope globs. |
| **Irreversibility list with human-approval requirement** | gstack's `/careful` and `/guard` warn before destructive commands but don't enforce a project-specific irreversibility set. |
| **ADR-0002 append-only invariant** | gstack has no convention for "this decision is settled, don't re-litigate." Compact's supersedence chain provides one. |
| **Tier-mismatch and silent-decisions audit** | gstack has no equivalent to "you said this was Tier 0 but the diff says Tier 2" or to a cumulative reversible-decisions log. |

### 11.2 What Compact gains from gstack

| gstack contribution | What Compact lacked |
|---|---|
| **`/freeze` PreToolUse hook** | Compact had a *planned* scope-enforcement hook. gstack ships it, deny-default, production-tested. Closes Compact's largest enforcement gap. |
| **`/codex` cross-model adversarial review** | Compact had a *planned* same-model adversarial subagent. gstack's `/codex` calls OpenAI — different vendor, different training, strictly more independent. |
| **`/qa` real-browser testing** | Compact's evidence parser was theoretical without a QA tool. gstack's `/qa` clicks through actual flows in Chromium and writes regression tests. |
| **`/autoplan` and `/plan-{ceo,eng,design,devex}-review`** | Compact had a tier rubric but no temporal pipeline. gstack provides validated multi-perspective plan review with auto-decisions. |
| **`/ship`, `/land-and-deploy`, `/document-release`** | Compact had no release flow. gstack supplies: VERSION bump, CHANGELOG, PR creation, post-merge health check, doc updates. |
| **`/cso` security review** | Compact had nothing for OWASP/STRIDE. gstack supplies it with confidence-gated reporting. |
| **`/investigate` root-cause debugging with 3-fix limit** | Compact had no anti-loop mechanism. gstack stops after 3 failed fixes. |
| **`/retro` and `/learn`** | Compact had no per-session memory or reflection. gstack supplies both, and the bridge protocol promotes recurring patterns to ADRs. |
| **22MB ML classifier + canary tokens for prompt-injection defense** | Compact had no security layer for browser-based agent work. gstack's two-classifier agreement defense closes this. |
| **`/pair-agent` for cross-vendor coordination** | Compact had no story for multiple agents from different vendors working in parallel. gstack provides scoped tokens, tab isolation, rate limiting. |
| **`/gstack-upgrade` self-update** | Compact's update model is "edit ADRs and ship a new version." gstack supplies a one-command upgrade path for the workflow layer. |

### 11.3 Where they jointly create a new property

Several effects only emerge from the combination:

- **Tier-adaptive ceremony.** gstack alone runs full ritual on every
  task; Compact alone has the rubric but no ritual to gate. Together:
  Tier 0 has zero overhead, Tier 2 has the full pipeline. This is the
  BMAD-style scale-adaptation neither tool has individually.
- **Charter-driven scope enforcement.** Compact's charter declares
  `in-scope`; gstack's `/freeze` enforces it via PreToolUse. Either
  alone is weaker.
- **Recurring-pattern → ADR promotion.** gstack's `/learn` accumulates
  patterns; Compact's ADR index accepts them. The ≥3-occurrence
  threshold is the bridge: high-confidence patterns graduate to
  immutable governance.
- **Cross-model review feeding governance decisions.** gstack's
  `/codex` produces disagreements; Compact's ADR system accepts them
  as decision artifacts. A `/codex` disagreement that's overridden
  becomes a permanent record explaining why.

## 12. Lifecycle of a task

### 12.1 Tier 0 (patch)
1. Agent reads cache prefix (cached after first session, ~free).
2. Agent makes the single-file edit.
3. Standard commit. No charter. No skills.
4. Cache prefix unchanged → next task starts cache-warm.

**Cost:** prefix read (cached), edit, commit. Zero ceremony.

### 12.2 Tier 1 (feature)
1. Agent reads cache prefix.
2. Agent writes `tasks/<id>.charter.md` (Tier 1, in-scope globs,
   out-of-scope, linked ADRs, acceptance evidence).
3. Agent symlinks `agent-context/30-active-charter.md` → charter file.
4. Agent invokes `/freeze` per the deepest-common-parent rule.
5. Implementation. Reversible defaults logged to
   `silent-decisions-log.md`; irreversibles ask one blocking question.
6. `/review` produces a bug list; agent applies obvious fixes.
7. `/qa` (if UI) writes outputs under `~/.gstack/projects/<slug>/qa/`.
8. Agent populates `tasks/<id>.evidence.md` from gstack outputs.
9. `/codex` (recommended) for second opinion.
10. `/ship` after evidence is complete.

**Cost:** one charter, one evidence file, one freeze. ~6 skill invocations.

### 12.3 Tier 2 (architectural)
1. Agent reads cache prefix.
2. `/office-hours` surfaces assumptions.
3. `/autoplan` runs CEO + design + eng + DX review on the plan.
4. Agent writes the charter (no `Charter-Approved-By:` yet).
5. **Human reviews and adds approval trailer in a separate commit.**
6. Agent verifies trailer is from a non-agent identity.
7. Agent writes the new ADR(s); appends to `10-adr-index.md`.
8. `/freeze` per charter.
9. Implementation, with `/investigate` if root cause is unclear.
10. `/review`, `/codex` (mandatory), `/qa` (if UI), `/cso` (if security).
11. Evidence collection.
12. `/ship` → `/land-and-deploy` → `/document-release`.
13. `/retro` within 24h. Recurring learnings → ADR promotion.

**Cost:** highest, but the ratchet effect is permanent: the new ADR
prevents this question from being re-litigated on every future task.

## 13. Multi-agent + human topology

Compact + gstack supports several concurrency patterns:

```
                        ┌────────── Lead agent (orchestrator) ──────────┐
                        │ Reads cache prefix + active charter            │
                        │ Tracks decisions, logs silent defaults         │
                        │ Never implements (keeps own cache warm)        │
                        └────────────┬──────────────────────────────────┘
                                     │
              ┌──────────────────────┼──────────────────────────┐
              ▼                      ▼                          ▼
    ┌──────────────────┐  ┌──────────────────┐    ┌──────────────────────┐
    │ Implementer      │  │ Verifier         │    │ Adversarial reviewer │
    │ (gstack /freeze) │  │ (gstack /qa,     │    │ (gstack /codex)      │
    │ Charter scope    │  │  /review)        │    │ Cross-model          │
    └──────────────────┘  └──────────────────┘    └──────────────────────┘

                                 │
                                 ▼
                ┌───────────────────────────────────┐
                │      Human (approval gate)        │
                │  - Tier 2 charter approval        │
                │  - /codex disagreement resolution │
                │  - Irreversibility list edits     │
                └───────────────────────────────────┘
```

- **Lead never implements.** Stays small, stays cache-warm, makes
  decisions and tracks state.
- **Implementer subagent** scoped to charter via `/freeze`.
- **Verifier subagent** runs `/qa` and `/review`. With permission
  scoping, it has read-only access to test files (so it cannot make
  tests pass by modifying them).
- **Adversarial reviewer** is `/codex` — different vendor entirely.
- **Human** approves only what the constitution requires: Tier 2
  charters, irreversibility-list-touching changes, codex disagreements.
- **Multiple agents from different vendors** can coordinate via
  gstack's `/pair-agent` (scoped tokens, tab isolation).

## 14. Failure modes & honest limits

The system has known soft spots. Documenting them prevents over-claim.

### 14.1 Cache architecture is a vendor bet
Claude's prompt-cache TTL, byte-stability requirements, and pricing
could change. Mitigation: the data layer (Markdown ADRs, charters,
indexes) is portable; only the cache discipline depends on Anthropic
primitives.

### 14.2 Silence-as-proceed degrades via habituation
After ~50 silent-proceeds, humans stop reading defaults carefully.
The cumulative log in `silent-decisions-log.md` and weekly digest
(future) are the mitigation, but the protocol's softest underbelly.

### 14.3 Tier mismatch detector is gameable
PR-splitting attack: agent ships two Tier 0 PRs that cumulatively
equal a Tier 2 change. No clean fix without cross-PR analysis (a
periodic job that diffs main against last-week-main). Accepted gap.

### 14.4 Evidence parser is fakeable
Tests can be written that pass without exercising the change.
Coverage delta and mutation testing partially mitigate, but determined
faking is hard to prevent automatically. Mitigation: verifier subagent
runs with read-only permissions on test files.

### 14.5 Onboarding tax
A new contributor or fresh agent session has to read the constitution,
tier rubric, ADR index, and skill bindings before useful work. Below
some project-size threshold (~10k LoC, <3 contributors, <3 months
expected lifetime), the system may cost more than it saves.

### 14.6 ~150-line AGENTS.md research finding
Frontier LLMs follow ~150-200 instructions per session reliably; more
degrades. AGENTS.md is currently 58 lines, the cache prefix is ~341
lines aggregate. Both are within budget but the ADR index is the
unbounded-growth risk; the ≥90-day archive policy is the mitigation.

### 14.7 What no governance system can fix
- Agents that can edit `.claude/`, `agent-context/0*`, hooks, or ADRs
  with full permissions. **Permission-deny on these paths is
  non-negotiable.**
- Agents whose harness ignores Markdown context entirely. Compact
  cannot govern an agent that doesn't read its files.
- Bad humans approving bad charters with rubber-stamp culture. The
  approval bottleneck is real; there is no purely-technical fix.

## 15. Roadmap

### 15.1 Implemented (this scaffold)
- Cache-aligned `agent-context/` with frozen prefix (00-05, 10, 20, 30)
- Append-only `docs/adr/` with 4 seed ADRs and timestamp prefixes
- Charter / evidence / silent-decisions / pending-decisions templates
- Tier rubric, silence-as-proceed protocol, irreversibility list
- gstack 1.26.3.0 installed and bridged via `04-skill-bindings.md` and
  `05-bridge-protocol.md`
- AGENTS.md (and CLAUDE.md symlink) routing to the bridge

### 15.2 Next (in order of ROI)
1. **`bin/compact-bind`** — auto-compute charter's deepest common parent
   and invoke `/freeze`. Removes a manual step at task start.
2. **`bin/compact-collect-evidence`** — pipe gstack's `/qa` and `/review`
   outputs from `~/.gstack/projects/<slug>/` into `tasks/<id>.evidence.md`.
3. **Permission denylist in `.claude/settings.json`** — block edits to
   `.claude/`, `docs/adr/`, `agent-context/0*-*.md`, hooks, and the
   gstack global skills directory. Without this, every other defense is
   bypassable.
4. **Pre-commit hook** that verifies `Charter-Approved-By:` was added by
   a non-agent commit (Tier 2).
5. **GitHub Action `compact-check`** as a required status check —
   server-side mirror of the pre-commit hook.
6. **First MODULE.md** when the first real code module exists.
7. **Weekly silent-decisions digest** — surface concerning patterns
   (irreversible-adjacent, recurring, contradicting older defaults).
8. **Tier-mismatch detector** comparing declared tier against actual
   diff scope.

### 15.3 Deliberately deferred or dropped
- Compact's adversarial review subagent → dropped (replaced by `/codex`).
- Compact's PreToolUse scope hook → dropped (replaced by `/freeze`).
- Compact's evidence parser as primary mechanism → reduced to a thin
  layer over gstack's `/qa` artifacts.
- Compact's plan-review subagent → dropped (replaced by `/autoplan`).
- Cross-PR cumulative-tier detector → deferred indefinitely; gap accepted.
- Per-file Tessl-style "DO NOT EDIT" annotations → never adopted; too
  granular, low ROI, empirically ignored.

## 16. References

### 16.1 Internal
- [`AGENTS.md`](./AGENTS.md) — entry point and read order
- [`agent-context/00-system.md`](./agent-context/00-system.md) — operating loop
- [`agent-context/01-constitution.md`](./agent-context/01-constitution.md) — invariants
- [`agent-context/02-tier-rubric.md`](./agent-context/02-tier-rubric.md) — tiers
- [`agent-context/03-question-protocol.md`](./agent-context/03-question-protocol.md) — silence-as-proceed
- [`agent-context/04-skill-bindings.md`](./agent-context/04-skill-bindings.md) — tier→skill mapping
- [`agent-context/05-bridge-protocol.md`](./agent-context/05-bridge-protocol.md) — handshakes
- [`docs/adr/`](./docs/adr/) — full ADR text
  - ADR-0001 — Markdown is the data layer
  - ADR-0002 — Append-only governance
  - ADR-0003 — Claude Code is the primary harness
  - ADR-0004 — Integrate gstack as the workflow engine

### 16.2 External
- [garrytan/gstack](https://github.com/garrytan/gstack) — workflow engine
- [Inside Garry Tan's AI Coding Setup (YC Library)](https://www.ycombinator.com/library/OW-inside-garry-tan-s-ai-coding-setup)
- [Codified Context paper (arxiv 2602.20478)](https://arxiv.org/abs/2602.20478) — academic basis for hot/cold context split
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) — origin of the scale-adaptive ceremony idea
- [GitHub Spec-Kit](https://github.com/github/spec-kit) — spec-driven development reference
- [AGENTS.md spec](https://agents.md/) — cross-tool documentation convention
- [LLM-based Agents Suffer from Hallucinations: A Survey (arxiv 2509.18970)](https://arxiv.org/html/2509.18970v1)
