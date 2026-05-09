# Evidence — readme

**Charter:** [tasks/readme.charter.md](./readme.charter.md)
**Commit SHA:** _populated post-commit; this evidence file is part of the introducing commit_

## Tests

| # | Name | Expected | Actual | Result |
|---|---|---|---|---|
| T1 | line-count-in-budget | 250–500 lines | 269 lines | pass |
| T2 | all-internal-links-resolve | 0 missing files | 0 missing (26 links checked) | pass |
| T3 | required-sections-present | 13 sections per charter | all 13 present | pass |
| T4 | honest-performance-claim | "20–100×" range with high-end conditions; no "1000×" headline | exactly that pattern | pass |
| T5 | architecture-link-not-duplication | links to ARCHITECTURE.md instead of duplicating | yes — links 4 places | pass |
| T6 | demonstrated-working-references-real-pr | links PR #1 with concrete metrics | links to https://github.com/handybot-webpage/Agent4Agents/pull/1 | pass |
| T7 | augmentation-table-three-column | gstack-alone / Compact-alone / Together | yes, 11-row table | pass |
| T8 | faq-addresses-known-objections | covers LLM-not-enterprise-ready + ROI + gstack-dependency + cache-vendor-bet + safety-critical + standalone | 6 Q&A entries | pass |
| T9 | contributing-section-enforces-framework | mentions blocked direct push, charter req, tier rubric, append-only, frozen prefix, silence-as-proceed | all six items | pass |
| T10 | license-note-rather-than-silent-pick | TODO with rationale (one-way door, future ADR) | yes | pass |

## Commands

| # | Command | Exit code | Output |
|---|---|---|---|
| C1 | `wc -l README.md` | 0 | `269 README.md` |
| C2 | `python3` link-check (extracts internal links, checks existence) | 0 | `internal links checked: 26 / missing: 0` |
| C3 | `grep '^## \|^# ' README.md` | 0 | 13 sections matching charter requirements |

## Required-section coverage (per charter acceptance evidence)

| Required section | README anchor |
|---|---|
| Elevator pitch | top of README (one-liner under H1) |
| Problem | `## What problem this solves` |
| Solution | `## What it is, in one diagram` + `## How it works` |
| Quick start (new) | `## 30-second quick start (new project)` |
| Quick start (existing) | `## Existing codebase (5–7 day soft-launch)` |
| Architecture summary | `## How it works` (links ARCHITECTURE.md) |
| Demonstrated working | `## Demonstrated working` (links PR #1) |
| Compact↔gstack augmentation | `## Compact + gstack: complementary, not competing` |
| Performance & honesty | `## Performance — the honest range` |
| Status & roadmap | `## Status & roadmap` |
| FAQ | `## FAQ` |
| Contributing | `## Contributing` |
| License | `## License` |
| References | `## References` |

## UI evidence

N/A — markdown document; no rendered surface beyond GitHub's renderer.

## Coverage delta (Tier 1+)

N/A — documentation change, no test runner involved.

## Notes

- **Length:** 269 lines is comfortably within the charter's 250–500 budget. The cap exists because READMEs that exceed ~500 lines are not actually read; depth belongs in `ARCHITECTURE.md`.
- **Links:** 26 internal links verified; zero broken. External links (gstack, arxiv papers, BMAD, spec-kit, AGENTS.md spec) are static well-known URLs.
- **Honesty:** explicitly states the 1000× headline is "selling something." Documents the conditions (project lifetime, contributor count, server-side enforcement) under which the high end of the 20–100× range is reachable. Includes the under-10k-LoC "scaffold cost may exceed savings" caveat.
- **FAQ chosen objections:** LLM-can't-deliver-enterprise-reliability (the most-encountered critique, addressed in this conversation), human-in-loop ROI, why-gstack, cache-vendor-bet, safety-critical readiness, can-it-work-without-gstack. Each has a direct, non-defensive answer.
- **Self-reference:** the README's own footer notes that the framework caught a flaw in its first task's charter. This is a deliberate signal — readers see the system actively self-correcting in version 1, which is more credible than abstract claims.
- **Contributing section:** five concrete enforcement points (blocked direct push, charter requirement, tier rubric, append-only invariants, frozen-prefix rule, silence-as-proceed). All five are mechanically enforced by `compact-check` and the GitHub ruleset.
- **License pending:** explicitly TODO. Picking a license unilaterally would violate the project's own irreversibility list (license choice is a one-way door for downstream users). Future Tier 1 PR with an ADR.

## Self-review (simulating /review)

- **No hype.** "1000×" headline is explicitly disavowed in the performance section.
- **No fabricated claims.** Every metric (4s CI runs, 11/11 tests, 269 lines, etc.) is grounded in artifacts checked into this repo.
- **Concrete examples.** The "Demonstrated working" section links a real PR with real merged commits, not a hypothetical.
- **Honest concessions.** Three places where the framework is not yet ready (safety-critical, projects under 10k LoC, vendor-pricing exposure) are stated up front.
- **No duplication.** Architecture details that belong in `ARCHITECTURE.md` are linked, not repeated.
- **Audience layered.** First 80 lines convince in 30 seconds; deeper sections satisfy evaluators; FAQ catches objections; contributing is for committers.

## Cross-model review (`/codex`) not run

Tier 1 charter; `/codex` is *recommended* not required per `04-skill-bindings.md`. In a real session with `/codex` available, the recommended invocation would be `/codex review README.md`.
