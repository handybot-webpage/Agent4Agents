# Charter — vic-benchmark

**Tier:** 2
**Goal:** Scaffold a paper-inspired but domain-shifted benchmark — Vehicle Interior Cleaning (VIC) — using NVIDIA Isaac Sim. Inspired by [CleanUpBench (arxiv 2508.05543)](https://arxiv.org/abs/2508.05543) (indoor sweeping+grasping with mobile manipulator on Isaac Sim). Domain-shifted to vehicle interiors: smaller enclosed space, occluded geometry, vehicle-specific clutter classes, damage-avoidance metric.

## Why Tier 2
- Adds a new top-level module (`benchmarks/`) — first module in the project.
- Introduces a new domain (robotics simulation) and a heavy irreversibility-list dependency (Isaac Sim + Isaac Lab, `pip install isaaclab`-class).
- Requires a new ADR (ADR-0005) documenting both the benchmark scope and the sim-engine choice.
- Per `02-tier-rubric.md`: cross-module + new public API + irreversibility-list touch = Tier 2.

## In-scope
- `benchmarks/vehicle-interior-cleaning/**` (new subtree, ~15–20 files)
- `docs/adr/2026-05-09-0005-vic-benchmark.md` (new ADR)
- `agent-context/10-adr-index.md` (append ADR-0005 row — append-only)
- `agent-context/20-module-index.md` (append new module row — append-only)
- `agent-context/30-active-charter.md` (cache tail swap)
- `tasks/vic-benchmark.evidence.md`
- `tasks/silent-decisions-log.md` (append-only)

## Out-of-scope
- `agent-context/0*-*.md`, `1[1-9]-*.md`, `2[1-9]-*.md` (frozen prefix, except the two append-only indexes above)
- `bin/**`, `.github/**`, `.claude/**` (governance plumbing)
- `AGENTS.md`, `ARCHITECTURE.md`, `README.md` (docs)
- All other ADRs (ADR-0001 through ADR-0004 are immutable)
- An actual *running* simulation. The scaffold is correct-in-shape; full execution requires Linux + NVIDIA RTX (the user's macOS is not the deploy target).

## Linked ADRs
- ADR-0001 — Markdown is the data layer (SPEC.md, MODULE.md, configs in YAML)
- ADR-0002 — Append-only governance (ADR index, module index extended via append)
- ADR-0003 — Claude Code is the primary harness (irrelevant to runtime; benchmark runs without an agent harness)
- **ADR-0005 (new)** — Vehicle Interior Cleaning benchmark scope + Isaac Sim selection

## Linked MODULE.md
- `benchmarks/vehicle-interior-cleaning/MODULE.md` (created by this charter)

## Acceptance evidence
- **Spec coverage:** SPEC.md defines ≥4 cleaning tasks (sweep_floor, pickup_objects, spot_clean_seat, full_clean), ≥5 metrics (TCR, SE, MQ, CP, DA), ≥3 vehicle classes (sedan, SUV, hatchback), train/eval-known/eval-novel split.
- **Module contract:** MODULE.md lists owner, public API surface, invariants, linked ADRs.
- **Code shape:** Python package `vic` under `src/`, with `env.py`, `tasks.py`, `metrics.py`, `baselines/heuristic.py`, `eval.py`, `configs/vehicles.yaml`. Imports gracefully degrade when Isaac Sim isn't installed (so dev on macOS works for non-sim parts).
- **Tests:** pure-Python tests for metrics + config parsing. Run on macOS without Isaac. ≥4 test cases pass.
- **Setup docs:** `benchmarks/vehicle-interior-cleaning/README.md` documents Linux+RTX requirement, install steps, how to run a baseline rollout.
- **Honest limits:** README + ADR explicitly state what's NOT implemented (actual sim run, RL training, real vehicle assets).

## Charter-Approved-By
**handybot-webpage** (project owner, via `AskUserQuestion` irreversible-decision approval on 2026-05-09 — explicit Isaac Sim selection over MuJoCo/Newton with full tradeoff visibility).

## /codex review
**Required** per Tier 2 (`04-skill-bindings.md`). Not run in this development session because `/codex` requires a live Claude Code session with gstack skills active. The recommended invocation is `/codex review benchmarks/vehicle-interior-cleaning/` after merge — a follow-up Tier 0/1 task can capture the codex transcript.

## /qa review
**N/A.** The benchmark has no UI surface. `/qa` is for browser-based UX validation.

## /cso review
**Recommended.** Isaac Sim install path runs untrusted USD assets; baseline policies execute robot motions in a virtual environment without sandboxing concerns. Risk profile is low for the scaffold (no network, no shell-out). Defer `/cso` to when actual sim assets are imported.

## What this scaffold does NOT do (honest scope)
- Does not run the simulator on this machine (macOS Apple Silicon; Isaac Sim is Linux+RTX only).
- Does not provide trained RL baselines — only heuristic/scripted policies.
- Does not include real vehicle USD assets — generates procedural primitive-mesh approximations.
- Does not implement a leaderboard or evaluation server — local CLI only.
- Does not match CleanUpBench numerically — different domain, different metrics. Inspired-by-name, not reproducing-results.
