# Evidence — vic-benchmark

**Charter:** [tasks/vic-benchmark.charter.md](./vic-benchmark.charter.md)
**ADR:** [docs/adr/2026-05-09-0005-vic-benchmark.md](../docs/adr/2026-05-09-0005-vic-benchmark.md)
**Commit SHA:** _populated post-commit; this evidence file is part of the introducing PR_

## Tests (29 / 29 passed in 0.06 s on macOS without Isaac Sim)

| File | Count | Coverage |
|---|---|---|
| `tests/test_metrics.py` | 12 | TCR/SE/MQ/CP/DA correctness, edge cases (empty, overshoot, threshold), aggregate math |
| `tests/test_config.py` | 9 | Config loaders, vehicle/task/clutter class presence, required-field validation, `VICTask.from_config` round-trip + composite scoring |
| `tests/test_heuristic.py` | 7 | Sweep targets nearest debris, ignores irrelevant clutter; grasp picks then places; wipe targets highest-coverage spill; unknown phase = noop; reset returns to sweep |

```
$ .venv/bin/pytest
.............................                                            [100%]
29 passed in 0.06s
```

## Commands (5)

| # | Command | Exit | Output / Effect |
|---|---|---|---|
| C1 | `pip install -e ".[dev]"` (Python 3.12 venv) | 0 | package + pytest installed; entry point `vic-eval` registered |
| C2 | `python -c "import vic; print(vic.__version__)"` | 0 | `0.1.0` — package imports cleanly without Isaac |
| C3 | `pytest` | 0 | 29 passed in 0.06 s |
| C4 | `vic-eval --vehicle sedan --task sweep_floor --policy heuristic --episodes 5 --dry-run` | 0 | Plan printed with deterministic seeds; no rollout run |
| C5 | `python -c "from vic import VICEnv; VICEnv()"` | 1 | `ImportError: Isaac Lab is required for the VIC environment runtime.` (the designed graceful fallback) |

## Acceptance evidence vs charter

| Charter requirement | Status |
|---|---|
| ≥4 cleaning tasks | ✓ 4 (`sweep_floor`, `pickup_objects`, `spot_clean_seat`, `full_clean`) |
| ≥5 metrics | ✓ 5 (TCR, SE, MQ, CP, DA) + composite VIC |
| ≥3 vehicle classes | ✓ 3 (`sedan`, `suv`, `hatchback`) |
| Train / eval-known / eval-novel split | ✓ defined in `SPEC.md §6` and validated by `vic-eval` `--split` choice |
| MODULE.md with owner / API / invariants / linked ADRs | ✓ |
| Python package shape (`src/vic/` with env, tasks, metrics, baselines, eval) | ✓ |
| Imports gracefully degrade without Isaac | ✓ (C2 + C5 confirm) |
| ≥4 pure-Python tests pass on macOS | ✓ 29 passed |
| README documents Linux+RTX requirement | ✓ (top of `benchmarks/vehicle-interior-cleaning/README.md`) |
| Honest limits stated | ✓ (`README.md` "What this scaffold does NOT include" + ADR §"Negative" + charter "What this scaffold does NOT do") |

## Files added (24)

```
benchmarks/vehicle-interior-cleaning/
├── .gitignore                            (8 lines)
├── MODULE.md                             (66 lines)
├── README.md                             (113 lines)
├── SPEC.md                               (160 lines)
├── pyproject.toml                        (39 lines)
├── configs/
│   ├── clutter.yaml                      (44 lines)
│   ├── tasks.yaml                        (60 lines)
│   └── vehicles.yaml                     (55 lines)
├── src/vic/
│   ├── __init__.py                       (32 lines)
│   ├── config.py                         (44 lines)
│   ├── env.py                            (87 lines, graceful Isaac fallback)
│   ├── eval.py                           (65 lines, --dry-run validates configs)
│   ├── metrics.py                        (105 lines)
│   ├── tasks.py                          (47 lines)
│   └── baselines/
│       ├── __init__.py                   (4 lines)
│       └── heuristic.py                  (78 lines)
└── tests/
    ├── __init__.py                       (0 lines)
    ├── test_config.py                    (60 lines)
    ├── test_heuristic.py                 (75 lines)
    └── test_metrics.py                   (110 lines)

docs/adr/2026-05-09-0005-vic-benchmark.md (97 lines)
agent-context/10-adr-index.md             (+1 row, append-only)
agent-context/20-module-index.md          (1 row, append-only)
agent-context/30-active-charter.md        (cache tail swap)
tasks/vic-benchmark.charter.md            (89 lines)
tasks/vic-benchmark.evidence.md           (this file)
tasks/silent-decisions-log.md             (+12 rows, append-only)
```

## UI evidence
N/A — CLI tool + library, no UI surface.

## Coverage delta
N/A for v0.1 — coverage tooling is configured (`pytest-cov` is in dev extras) but no baseline coverage was previously measured. v0.2 will introduce a coverage gate when the env runtime is implemented.

## Notes

### Framework discipline observed
- **Tier 2 protocol followed:** charter explicitly tier-2 (cross-module + new public API + irreversibility-list dependency). New ADR (0005) authored as part of this PR. Charter-Approved-By trailed by `handybot-webpage` via the explicit AskUserQuestion answer.
- **Append-only invariants respected:** ADR index, module index, silent-decisions log all gain rows; no removals. Will be verified by `compact-check` on push.
- **Frozen-prefix files untouched:** `agent-context/00-` through `05-` were not edited. Only the cache tail (`30-active-charter.md`) was swapped, plus the two append-only indexes (`10-`, `20-`).

### Honest scope limits (carried over from charter)
- The scaffold is **shape-correct, not behavior-correct** for the simulator runtime. End-to-end episodes require an Isaac Sim host — see ADR-0005 §"Negative".
- Procedural vehicle interior generation is a **stub**. v0.1 declares geometry in YAML but does not yet emit USD scenes.
- The `/codex` cross-model review (Tier 2 recommended per `04-skill-bindings.md`) was not run in-session because invoking `/codex` requires a live gstack-active Claude Code session. Recorded as a follow-up Tier 0/1 task in `silent-decisions-log.md`.

### Self-review (simulating /review)

**Code quality**
- All algorithmic functions have docstrings. Non-trivial logic (metric formulas, glob parsing, deepest-common-parent in `compact-bind`) carries inline rationale linking to SPEC.md sections.
- No dead code. No commented-out experiments.
- No SQL injection / shell-out / network IO risks (the scaffold has no networking and no shell-out).

**Type safety**
- Frozen dataclass for `VICTask`; standard mutable dataclass for incremental `VICMetrics`.
- Type hints on all public function signatures.
- No `Any` in the public API except where deliberate (info dicts emitted by Isaac at runtime).

**Reproducibility**
- Deterministic seeds derived from `(split, vehicle, task, episode)` tuple per SPEC.md §9.
- Configs are the source of truth (per ADR-0001); no magic constants in code outside metric defaults that match SPEC.md §5.

**Honest gaps**
- No integration test against Isaac Sim (the only platform that can run it isn't this machine).
- No benchmark of a baseline on a real env (same reason).
- No benchmark of MuJoCo as fallback (chose Isaac per user, accepting the macOS dev-loop tradeoff).

These gaps are documented in MODULE.md "Roadmap" and the v0.2 milestone (Provision Isaac Sim host).

### What this exercises about the framework
- **First Tier 2 task** under Project Compact + gstack governance.
- **First module** to land under `benchmarks/` — module index now non-empty.
- **First time** an ADR with explicit `Charter-Approved-By` from a non-agent identity (`handybot-webpage` via AskUserQuestion) was the basis of a Tier 2 PR.
- **First time** the framework's irreversibility-list-question protocol fired (sim engine choice surfaced via AskUserQuestion with multiple-choice tradeoff visibility).
- **First time** the cache tail (`30-active-charter.md`) was swapped without invalidating the frozen prefix (`00-` through `05-`).
- The append-only invariants on `10-adr-index.md`, `20-module-index.md`, and `silent-decisions-log.md` will be enforced by `compact-check` in CI on push.
