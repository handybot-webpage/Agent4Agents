# Project Compact

**Governance substrate for multi-agent + human software development.** Pairs with [gstack](https://github.com/garrytan/gstack) as the workflow engine.

> If gstack is the workflow, Compact is the constitution.

[![compact-check](https://github.com/handybot-webpage/Agent4Agents/actions/workflows/compact-check.yml/badge.svg)](https://github.com/handybot-webpage/Agent4Agents/actions/workflows/compact-check.yml)
[![status: actively developed](https://img.shields.io/badge/status-actively%20developed-green)](#status--roadmap)
[![docs](https://img.shields.io/badge/docs-ARCHITECTURE.md-blue)](./ARCHITECTURE.md)

---

## What problem this solves

Vanilla agentic coding fails at scale in four documented ways:

1. **Bogus work.** Agents invent adjacent tasks ("while I'm here…"), producing changes nobody asked for.
2. **Whack-a-mole on decisions.** Agents re-litigate settled architectural questions because they cannot tell which decisions are firm.
3. **Decision fatigue.** Agents pepper humans with clarifying questions that should have been inferred or batched.
4. **Token + time waste.** Each turn re-reads context, re-derives conventions, re-discovers state — costs that compound across thousands of turns and dozens of contributors.

Project Compact is architected so the **rules are mechanically enforced, not advisory**. The same insight that lets enterprise software teams produce reliable output from individually-unreliable humans (process, hooks, peer review, audit logs, version control) is applied to agents.

## What it is, in one diagram

```
┌────────────────────────────── AGENTS.md ──────────────────────────────┐
│              "Read agent-context/ in numerical order. Use gstack."    │
└──────────────────────────────────┬────────────────────────────────────┘
                                   ▼
┌──────────────── agent-context/  (cached prefix, ~14KB) ───────────────┐
│ 00-system  01-constitution  02-tier-rubric  03-question-protocol      │
│ 04-skill-bindings  05-bridge-protocol                                  │
│ 10-adr-index (append-only)  20-module-index (append-only)             │
│ 30-active-charter (only cache-tail mutation, swaps per task)          │
└─────────┬─────────────────────────────────────────────┬───────────────┘
          ▼                                             ▼
┌─────────────────────┐              ┌──────────────────────────────────┐
│ docs/adr/           │              │ ~/.claude/skills/gstack/         │
│ append-only ADRs    │              │ 46 skills as slash commands      │
│ "law" of project    │              │ /freeze /codex /qa /autoplan     │
└─────────┬───────────┘              │ /ship /review /cso /retro …      │
          │                          └──────────────────────────────────┘
          ▼
┌───────────────────────────────────────────────────────────────────────┐
│ tasks/<id>.charter.md     declared scope, tier, evidence acceptance   │
│ tasks/<id>.evidence.md    populated before "done"                     │
│ tasks/silent-decisions-log.md   audit trail of reversible defaults    │
│ tasks/pending-decisions.md      non-blocking ambiguities, parked      │
└───────────────────────────────────────────────────────────────────────┘
```

**Compact** owns the data layer (left): cache-aligned context, ADRs, charters, evidence, audit logs.
**gstack** owns the workflow engine (right): plan review, scope hooks, real-browser QA, cross-model review, ship discipline.
**Two bridge files** — [`04-skill-bindings.md`](./agent-context/04-skill-bindings.md) and [`05-bridge-protocol.md`](./agent-context/05-bridge-protocol.md) — wire them.

## At a glance

- **Cache-aligned context prefix.** Pays once per 5-min window per agent, reused across hundreds of turns. Yields ~30× reduction in prefix tokens alone.
- **Append-only ADRs with supersedence.** Settled decisions are immutable; re-litigation requires writing a new ADR. Filenames use timestamp prefixes (no merge-race on numbering).
- **Tier-adaptive ceremony.** Tier 0 patches pay zero overhead. Tier 1 features get charter + evidence. Tier 2 architectural changes get charter + evidence + new ADR + human approval.
- **Silence-as-proceed for reversibles.** Agents declare default + reasoning, proceed unless objected. Irreversibles (constitution-defined) always block. Both paths are audit-logged.
- **Server-side enforcement.** [`bin/compact-check`](./bin/compact-check) runs in CI as a [required status check](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets) with **no admin bypass**. Frozen-prefix files, accepted ADRs, and append-only logs are mechanically protected.
- **Plain Markdown data layer.** Portable across agent harnesses; survives a vendor or model change.

## 30-second quick start (new project)

```bash
# 1. One-time deps (~5 min, once per machine)
brew install oven-sh/bun/bun
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
cd ~/.claude/skills/gstack && ./setup --no-prefix

# 2. Bootstrap from this scaffold
NEW_PROJECT=~/Work/my-new-project
git clone https://github.com/handybot-webpage/Agent4Agents.git "$NEW_PROJECT"
cd "$NEW_PROJECT"
rm -rf .git && git init -b main
# customize agent-context/01-constitution.md (project intent + irreversibility list)
# add 5–8 first ADRs in docs/adr/  (language, runtime, data, deploy, …)
git add . && git commit -m "scaffold from Project Compact"
```

After this you have: cached context prefix, gstack workflow engine globally, charter+evidence templates ready, append-only ADRs ready. Open a session in the project root, point the agent at [`AGENTS.md`](./AGENTS.md), and start with a real task.

## Existing codebase (5–7 day soft-launch)

For a >10k-LoC repo, the honest cost is one engineering week (mostly in **decision archaeology** — extracting implicit ADRs from existing code).

```bash
cd ~/Work/your-existing-project
# 1. Drop in scaffold without clobbering
[ -f AGENTS.md ] && mv AGENTS.md AGENTS.md.preexisting
git clone https://github.com/handybot-webpage/Agent4Agents.git /tmp/compact-scaffold
cp -R /tmp/compact-scaffold/{AGENTS.md,CLAUDE.md,ARCHITECTURE.md,agent-context,docs,tasks,bin,.github,.gitignore} ./
# 2. Decision archaeology with agent assistance
# 3. Module mapping (one MODULE.md per top-level module)
# 4. Customize constitution (irreversibility list = your domain's danger paths)
# 5. Soft-launch: rules advisory week 1, soft-check week 2, hard-enforce week 3+
```

Full step-by-step instructions in [`ARCHITECTURE.md`](./ARCHITECTURE.md) §15.

## How it works

Three layers, each a deliberate choice about *where reliability lives*:

### 1. Substrate (Compact, always-on)
Cached context loaded into every agent session in numerical order. Forms a byte-stable prefix that hits Claude's prompt cache on every turn within the 5-min TTL. Append-only invariants (per [ADR-0002](./docs/adr/2026-05-05-0002-append-only-governance.md)) keep the prefix stable for hundreds of turns.

### 2. Workflow engine (gstack, on-demand)
46 skills as slash commands: `/freeze`, `/qa`, `/codex`, `/autoplan`, `/ship`, `/review`, `/investigate`, `/retro`, `/learn`, `/cso`, …  Compact's tier rubric decides *which* skills are required for which task; gstack provides the *how*.

### 3. Governance (Compact, per-task)
Charter declares scope, tier, evidence criteria. Evidence file links real artifacts (test names + outputs, screenshots, commit SHAs). Silent-decisions log audits every reversible default. Pre-merge `compact-check` enforces frozen-prefix protection, ADR immutability, and append-only invariants.

For depth: [ARCHITECTURE.md](./ARCHITECTURE.md) (595 lines) covers the design, augmentation matrix, lifecycle walkthroughs, multi-agent topology, failure modes, and roadmap.

## Demonstrated working

The framework is exercised on its own development. Real task, real PR, real artifacts:

- **[PR #1 — `compact-bind`](https://github.com/handybot-webpage/Agent4Agents/pull/1)** — first real Tier 1 task using the full lifecycle.
  - Direct push to `main` was **rejected by the ruleset** (`compact-check` required, no admin bypass).
  - The framework caught a real design flaw in this very PR's charter (overly broad `## In-scope` led to disjoint-roots in Tier 1). Resolution preserved as charter addendum per the append-only rule.
  - 11/11 inline tests passed; CI green in 4s.
  - Append-only invariant on `silent-decisions-log.md` and `pending-decisions.md` enforced.

Lifecycle artifacts you can read in this repo:

| Artifact | What it documents |
|---|---|
| [`tasks/compact-bind.charter.md`](./tasks/compact-bind.charter.md) | Tier 1 declaration with mid-task addendum |
| [`tasks/compact-bind.evidence.md`](./tasks/compact-bind.evidence.md) | 11 tests, 5 commands, scope rationale |
| [`tasks/silent-decisions-log.md`](./tasks/silent-decisions-log.md) | Reversible defaults with reasoning |
| [`tasks/pending-decisions.md`](./tasks/pending-decisions.md) | Open framework questions, parked for future ADRs |

## Compact + gstack: complementary, not competing

|  | gstack alone | Compact alone | Together |
|---|---|---|---|
| Workflow engine (plan review, QA, ship) | ✓ mature | — | ✓ |
| Real-browser testing (`/qa`) | ✓ Chromium | — | ✓ |
| Cross-model review (`/codex`) | ✓ via OpenAI | — | ✓ |
| Cache-aligned context | — | ✓ | ✓ |
| Append-only ADRs | — | ✓ | ✓ |
| Tier-adaptive ceremony | runs full ritual every task | rubric only, no ritual | ✓ scale-adapted |
| Scope enforcement | `/freeze` (opt-in) | charter declares scope | ✓ charter drives `/freeze` |
| Silence-as-proceed for reversibles | — | ✓ | ✓ |
| Server-side enforcement perimeter | — | ✓ | ✓ |
| Cross-tool data portability (markdown) | — | ✓ | ✓ |
| Cross-vendor agent coordination | ✓ `/pair-agent` | — | ✓ |

Either alone leaves real gaps. Combined: gstack supplies the validated workflow patterns; Compact supplies the discipline that makes gstack's outputs durable. Full augmentation matrix in [`ARCHITECTURE.md`](./ARCHITECTURE.md) §11.

## Performance — the honest range

The headline number is **20–100× compounded efficiency** vs ungoverned agent work. The high end requires:

- Project lifetime > 3 months (cache amortization needs volume)
- ≥3 active developers (multi-agent isolation has reasons to exist)
- Charters that are well-scoped (otherwise the cache tail invalidates often)
- Server-side enforcement perimeter actually live (without it, the system collapses to prose)

| Lever | Contribution | Mechanism |
|---|---|---|
| Prompt cache discipline | ~30× | byte-stable frozen prefix, append-only indexes |
| Right-sized context per agent | ~3× | ≤80-line AGENTS.md, time-windowed ADR index, JIT MODULE.md |
| Multi-agent isolation | ~2× | lead orchestrates, doesn't implement; subagents have own caches |
| Decision elimination | ~1.5× tokens, ~30× human time | silence-as-proceed, irreversibility-list-only blocking |
| Rework prevention | ~1.5× | charter scope + `/freeze` + adversarial review |

These don't fully compose — they share resources and partially overlap. The realistic compounded result is **80–150× on tokens, 10–30× on human time**, with the high end on long-running, high-volume projects. Anyone claiming 1000× is selling something.

For projects under ~10k LoC, fewer than 3 contributors, or under 3 months expected lifetime: **the scaffold cost may exceed the savings**. Use raw gstack only.

## Status & roadmap

**Implemented (v1.0)**

- Cache-aligned `agent-context/` with frozen prefix (00–05, 10, 20, 30)
- Append-only `docs/adr/` with 4 seed ADRs (timestamp-prefixed)
- Charter / evidence / silent-decisions / pending-decisions templates
- Tier rubric, silence-as-proceed protocol, irreversibility list
- gstack 1.26.x integration via [`04-skill-bindings.md`](./agent-context/04-skill-bindings.md) + [`05-bridge-protocol.md`](./agent-context/05-bridge-protocol.md)
- [`bin/compact-check`](./bin/compact-check) — Python, stdlib-only, three checks (frozen-prefix, ADR immutability, append-only)
- [`bin/compact-bind`](./bin/compact-bind) — auto-extracts charter scope for `/freeze`
- GitHub Action `compact-check` running on PRs and pushes to main
- Branch ruleset: required `compact-check`, no force-push, no deletion, **no admin bypass**

**Next, in ROI order**

1. `bin/compact-collect-evidence` — pipe `/qa` and `/review` outputs into `evidence.md` automatically
2. `--staged` mode on `compact-check` + local pre-commit hook for fast feedback
3. Permission denylist in `.claude/settings.json` for frozen paths
4. `Charter-Approved-By:` non-agent verification for Tier 2
5. Tier-mismatch detector (declared tier vs actual diff scope)
6. Coverage-delta gate on evidence files
7. First `MODULE.md` (when first real code module exists)

**Deferred or dropped**

- Compact's adversarial-review subagent → replaced by gstack `/codex`
- Compact's PreToolUse scope hook → replaced by gstack `/freeze`
- Cross-PR cumulative-tier detector → gap accepted, no clean fix
- Per-file `DO NOT EDIT` annotations → empirically ignored, low ROI

## FAQ

**"LLMs can't deliver enterprise reliability, predictability, or traceability."**
Correct about LLMs in isolation. Wrong about *systems built around* LLMs. The same architectural pattern that produces reliable enterprise software from individually-unreliable humans (process, hooks, audit logs) is applied here. The framework explicitly does not ask the LLM to be reliable; it asks the *envelope* (deterministic gates, append-only governance, server-side enforcement) to be reliable. Output reliability is inherited from the envelope when enforcement is mechanical and continuous.

**"Doesn't human-in-the-loop break ROI?"**
Only if humans are in the loop on *every* output. Compact concentrates human attention on irreversibles (auth, billing, migrations, dependency changes, public API breaks) and silence-proceeds on reversibles. The empirical attention budget is roughly: humans review one Tier 2 charter approval per architectural change, skim the silent-decisions log per PR, and ignore everything else. That is more attention than fully-autonomous agents (impossible) but far less than every-output review.

**"Why gstack? Why not build it all in Compact?"**
Building gstack from scratch would replicate ~46 mature, battle-tested skills. The maturity gap (gstack: tens of thousands of stars, real production usage) is not closeable in months. Compact contributes what gstack lacks (durable architectural memory, cache discipline, scale-adaptive ceremony) and defers to gstack on what it does well. See [ADR-0004](./docs/adr/2026-05-05-0004-gstack-integration.md).

**"What if Anthropic changes prompt-caching semantics?"**
The data layer (Markdown ADRs, charters, indexes) is portable. Cache discipline is the part that depends on Anthropic primitives. Pricing or TTL changes can swing the multiplier. Compact ships the substrate as plain Markdown specifically so the discipline survives a tool change.

**"What's safety-critical / regulated readiness?"**
Not yet. Frameworks demanding formal verification of every individual generation (medical devices, avionics, financial settlement) need more than Compact + gstack provides today. The roadmap does not promise to bridge that gap.

**"Can it work without gstack?"**
Yes — the data layer is independently useful. You'd lose `/freeze` (scope hook), `/codex` (cross-model review), `/qa` (real-browser testing), `/autoplan` (multi-perspective plan review), and the ship/release flow. You'd keep cache discipline, tier rubric, append-only ADRs, charter/evidence flow, and `compact-check` enforcement. Pragmatic for solo work or environments where gstack can't run.

## Contributing

This repo dogfoods its own framework. Contributing means:

1. **Direct push to `main` is blocked** by ruleset. Open a PR.
2. **Charter required** for any change beyond Tier 0. Use [`tasks/template.charter.md`](./tasks/template.charter.md) and place yours at `tasks/<slug>.charter.md`.
3. **Follow tier rubric** ([`agent-context/02-tier-rubric.md`](./agent-context/02-tier-rubric.md)):
   - Tier 0 — single file, no behavior change. No charter needed.
   - Tier 1 — feature within one module. Charter + evidence.
   - Tier 2 — cross-module / contradicts an ADR. Charter + evidence + new ADR + human approval.
4. **Append-only invariants** are enforced by `compact-check`. ADR bodies and audit logs cannot be rewritten — write a superseding ADR or append a new entry.
5. **Frozen prefix files** (`agent-context/0*-*.md`, `1*-*.md`, `2*-*.md`) require a Tier 2 charter in the same PR.
6. **Silence-as-proceed.** For reversible defaults, log to [`tasks/silent-decisions-log.md`](./tasks/silent-decisions-log.md) with reasoning + alternatives rejected. For irreversibles per the constitution, ask one blocking question.

If something seems wrong: open an issue, propose an ADR, or file a `pending-decisions.md` row. The framework is designed to be edited (see [ADR-0002](./docs/adr/2026-05-05-0002-append-only-governance.md)).

## License

TODO — license choice is a one-way door and deserves an ADR. Until then, treat as "all rights reserved" by the project authors. A future Tier 1 PR will introduce `LICENSE` plus an ADR documenting the choice.

## References

**Internal**

- [`AGENTS.md`](./AGENTS.md) — entry point and read order
- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — full design (595 lines)
- [`agent-context/`](./agent-context/) — cached context prefix (frozen 00–05, append-only 10/20, swap 30)
- [`docs/adr/`](./docs/adr/) — full ADR text
- [`tasks/`](./tasks/) — charter, evidence, decision-log templates and live entries

**External**

- [garrytan/gstack](https://github.com/garrytan/gstack) — the workflow engine this composes with
- [Codified Context: Infrastructure for AI Agents in a Complex Codebase (arxiv 2602.20478)](https://arxiv.org/abs/2602.20478) — academic basis for hot/cold context split
- [BMAD-METHOD](https://github.com/bmad-code-org/BMAD-METHOD) — origin of the scale-adaptive ceremony idea
- [GitHub Spec-Kit](https://github.com/github/spec-kit) — spec-driven development reference
- [AGENTS.md spec](https://agents.md/) — cross-tool documentation convention
- [Context Matters: Evaluating Context Strategies for Automated ADR Generation Using LLMs (arxiv 2604.03826)](https://arxiv.org/html/2604.03826) — empirical basis for time-windowed ADR index

---

<sub>Project Compact dogfoods its own framework: every change to this repo runs through a charter, evidence file, and `compact-check`. The framework caught a real flaw in its first task's own charter, surfaced it as a pending decision rather than silently patching, and merged the fix on a separate PR. That self-correcting property is the whole point.</sub>
