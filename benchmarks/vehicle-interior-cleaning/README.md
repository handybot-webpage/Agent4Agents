# Vehicle Interior Cleaning (VIC) Benchmark

> Embodied sweeping + grasping benchmark for mobile manipulators in vehicle cabins.
> Inspired by [CleanUpBench (arxiv 2508.05543)](https://arxiv.org/abs/2508.05543), domain-shifted to vehicle interiors.
> Built on NVIDIA Isaac Sim per [ADR-0005](../../docs/adr/2026-05-09-0005-vic-benchmark.md).

## Status: scaffold (v0.1)

The shape is correct. End-to-end simulation requires a Linux + RTX host and is **not** yet validated. The pure-Python parts (metric math, config parsing, task definitions, heuristic policy) **do** run and have unit tests on any platform.

## Platform requirements (for simulation)

| Component | Required |
|---|---|
| OS | Ubuntu 22.04+ (or RHEL 9). Isaac Sim does not support macOS or Windows |
| GPU | NVIDIA RTX 30/40-series or better, ≥16 GB VRAM |
| Driver | NVIDIA driver ≥ 535 |
| Disk | 50+ GB free for Isaac Sim assets and caches |
| Python | 3.10 (Isaac Lab requirement) |

For metric/config development on macOS or Linux without GPU: `pip install -e ".[dev]"` is enough — Isaac Sim is opt-in.

## Install — host with Isaac Sim

```bash
# 1. Install Isaac Sim (one-time, follow NVIDIA's installer)
#    https://docs.omniverse.nvidia.com/isaacsim/latest/installation/install_workstation.html

# 2. Install Isaac Lab on top
git clone https://github.com/isaac-sim/IsaacLab.git ~/IsaacLab
cd ~/IsaacLab && ./isaaclab.sh --install

# 3. Install this benchmark
cd /path/to/Agent4Agents/benchmarks/vehicle-interior-cleaning
pip install -e ".[isaac]"
```

## Install — dev only (macOS / no GPU)

```bash
cd benchmarks/vehicle-interior-cleaning
pip install -e ".[dev]"
pytest tests/
```

This installs `pyyaml`, `numpy`, `pytest`, and the package itself in editable mode. It does **not** install Isaac Sim. You can edit metric math, configs, and the heuristic policy and verify them with `pytest`. Anything that imports `omni.isaac.*` will raise a clear `ImportError` until Isaac is present.

## Quickstart (Isaac host)

```bash
# Run the heuristic baseline on 20 eval-known sedan episodes of the sweep_floor task
vic-eval --vehicle sedan --task sweep_floor --policy heuristic --episodes 20 --split eval-known

# Output: per-episode metrics + aggregate (TCR, SE, MQ, CP, DA, VIC composite)
```

## Quickstart (dev host, no Isaac)

```bash
# Verify pure-Python parts
pytest tests/

# Inspect configs
python -c "from vic.config import load_vehicles; print(load_vehicles())"

# Run heuristic policy against a recorded trace fixture
python -m vic.replay --trace tests/fixtures/sweep_floor_seed42.parquet
```

## Layout

```
benchmarks/vehicle-interior-cleaning/
├── README.md                # this file
├── MODULE.md                # module contract (owner, API, invariants)
├── SPEC.md                  # formal task and metric definitions
├── pyproject.toml           # package metadata, optional [dev] / [isaac] extras
├── configs/
│   ├── vehicles.yaml        # sedan, suv, hatchback configs
│   ├── tasks.yaml           # task parameters (lengths, counts, thresholds)
│   └── clutter.yaml         # clutter class definitions
├── src/vic/
│   ├── __init__.py          # public exports
│   ├── env.py               # Isaac Sim env wrapper (graceful import fallback)
│   ├── tasks.py             # task definitions
│   ├── metrics.py           # TCR, SE, MQ, CP, DA implementations
│   ├── config.py            # YAML config loaders
│   ├── baselines/
│   │   ├── __init__.py
│   │   └── heuristic.py     # scripted baseline policy
│   └── eval.py              # evaluation runner CLI
└── tests/
    ├── test_metrics.py
    ├── test_config.py
    └── test_heuristic.py
```

## What this scaffold does NOT include

- **Trained RL policies.** Out of scope until a separate Tier 2 charter introduces RL infra.
- **Real vehicle CAD models.** Asset licensing is its own irreversible decision.
- **A leaderboard.** v1.0 release will spec the submission format.
- **Sim-to-real.** Not on the roadmap.
- **Numerical reproduction of CleanUpBench results.** Different domain, different metrics.

## Contributing

Per the project's framework ([Project Compact](../../README.md)):

- Direct push to `main` is blocked. Open a PR.
- Charter required for Tier 1+. Templates in [`tasks/template.charter.md`](../../tasks/template.charter.md).
- Touching `agent-context/0*-*.md`, `1*-*.md`, `2*-*.md` requires a Tier 2 charter and ADR.
- Within this benchmark module: any change to public API surface (`vic.env.VICEnv`, `vic.metrics.VICMetrics`) is Tier 1+.

## References

- [CleanUpBench (arxiv 2508.05543)](https://arxiv.org/abs/2508.05543) — paper this benchmark is inspired by
- [ADR-0005](../../docs/adr/2026-05-09-0005-vic-benchmark.md) — sim engine selection rationale
- [SPEC.md](./SPEC.md) — formal benchmark spec
- [MODULE.md](./MODULE.md) — module contract
- [Isaac Lab](https://github.com/isaac-sim/IsaacLab) — RL framework on top of Isaac Sim
