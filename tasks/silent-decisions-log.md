# Silent decisions log (append-only)

Every reversible default the agent took without asking. PR templates link
this file; reviewers should skim entries since the last PR.

| Timestamp | Charter | Default chosen | Alternatives rejected | Notes |
|---|---|---|---|---|
| 2026-05-06 | compact-bind | Python (stdlib-only) | bash (fragile parsing); Go/Rust (compile step) | matches bin/compact-check; no new deps |
| 2026-05-06 | compact-bind | print directory only by default; `--invocation` flag for full `/freeze <dir>` command | print full /freeze by default (forces parse); JSON output (overkill) | composable with shell |
| 2026-05-06 | compact-bind | disjoint roots: Tier 1 exit 1, Tier 2 exit 0 with `.` + stderr warning | always succeed (defeats purpose); always fail (too strict for Tier 2) | matches bridge protocol §10.1 |
| 2026-05-06 | compact-bind | charter path is positional arg, default `agent-context/30-active-charter.md`, `-` for stdin | required explicit path (friction); env var (less obvious) | supports interactive + testing |
| 2026-05-06 | compact-bind | self-approval (Tier 1, single-developer) | request explicit human approval | per tier rubric §02 |
| 2026-05-09 | readme | scope = `README.md` only; framework-implicit paths (evidence, log, active charter) accessed per protocol | broader scope (would re-trigger compact-bind disjoint-roots issue) | matches addendum pattern from compact-bind charter |
| 2026-05-09 | readme | skip running compact-bind on this charter | run it and watch it falsely fail | known bug logged in pending-decisions; freeze scope manually = `.` |
| 2026-05-09 | readme | length target 250–500 lines | brief 100-line landing | substantial enough to convince evaluators; not so long it becomes ARCHITECTURE.md |
| 2026-05-09 | readme | claim 20–100× compounded efficiency with high-end conditions; no "1000×" headline | optimistic 100× flat; or skip the metric | matches Project Compact's honest-numbers section |
| 2026-05-09 | readme | license: leave as TODO with pointer to a future ADR | pick MIT now | license choice is a one-way door; deserves an ADR |
| 2026-05-09 | readme | self-approval (Tier 1) | request explicit human approval | per tier rubric §02 |
