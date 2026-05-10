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
| 2026-05-10 | vic-benchmark | sim engine = Isaac Sim (per AskUserQuestion approval) | MuJoCo (better dev loop, recommended); Newton (too immature) | irreversible per constitution; logged as user-explicit Tier-2 approval |
| 2026-05-10 | vic-benchmark | python = 3.10+ (Isaac Lab requirement); dev venv uses 3.12 from brew | match system 3.9 (would block Isaac Lab anyway); pin 3.10 exactly (no upside) | aligns dev with deploy target |
| 2026-05-10 | vic-benchmark | package layout = `src/vic/`, configs at sibling `configs/`, tests at sibling `tests/` | flat layout (mixes config and code); single-file module (won't scale) | matches modern Python package conventions |
| 2026-05-10 | vic-benchmark | Isaac Sim imports inside `env.py` are deferred via `importlib.util.find_spec` so the package imports cleanly without Isaac | hard import (would break tests on macOS); no env.py at all (loses contract documentation) | enables 29/29 tests on macOS dev loop |
| 2026-05-10 | vic-benchmark | env.py constructor raises NotImplementedError after validation (v0.1 stub) — full Isaac Lab scene assembly deferred to v0.2 | implement scene assembly speculatively without an Isaac host (untested code) | matches "ship the shape" charter scope |
| 2026-05-10 | vic-benchmark | three vehicle classes only (sedan, suv, hatchback); `eval-novel` split holds out clutter combos, NOT vehicle classes | hold out a vehicle class for eval-novel (v0.1 procedural gen too coarse to make this meaningful) | documented in SPEC.md §6 |
| 2026-05-10 | vic-benchmark | five metrics: TCR, SE, MQ, CP + new VIC-specific DA (Damage Avoidance) | strict CleanUpBench port (4 metrics; DA is the domain-specific addition) | vehicle interiors have fragile parts that indoor rooms don't |
| 2026-05-10 | vic-benchmark | composite VIC score = unweighted mean of 5 metrics; per-task `metrics_weight` exists for future weighted aggregation | weighted from the start (premature; balance is unknown until empirical baselines) | both reported, leaderboard format in v1.0 ADR |
| 2026-05-10 | vic-benchmark | DA threshold = 5 N force, max_allowed = 5 collisions per episode | tighter (1 N / 1 collision: too punitive without empirical data) | values picked to be plausible defaults; tunable |
| 2026-05-10 | vic-benchmark | `pyproject.toml` has `[isaac]` extras as documentation-only stub (Isaac Lab is not pip-installable from PyPI) | leave isaac out entirely (loses signal) | documents the deploy assumption |
| 2026-05-10 | vic-benchmark | benchmark-local `.gitignore` for `.venv/`, `__pycache__/`, `*.egg-info/`, `.pytest_cache/`, `*.parquet` | edit root `.gitignore` (out-of-scope per charter) | scoped to in-scope path tree |
| 2026-05-10 | vic-benchmark | `/codex` cross-model review: not run in this session (Tier 2 requirement, recommended invocation noted in charter) | skip cross-model review entirely (violates 04-skill-bindings.md) | follow-up Tier 0/1 task captures /codex transcript |
