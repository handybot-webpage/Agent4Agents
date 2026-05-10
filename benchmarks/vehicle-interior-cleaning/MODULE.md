# Module: vehicle-interior-cleaning

**Owner:** handybot-webpage
**Status:** scaffold (v0.1) — not yet runnable end-to-end on the developer's machine
**Public API:** the `vic` Python package + the `vic-eval` CLI

## Purpose
Embodied benchmark for cleaning vehicle interiors using a mobile manipulator
(mobile base + 6-DoF arm + sweeping mechanism). Inspired by CleanUpBench
(arxiv 2508.05543). Built on NVIDIA Isaac Sim per ADR-0005.

## Public API

```python
from vic import VICEnv, VICTask, VICMetrics, HeuristicPolicy

env = VICEnv(vehicle_class="sedan", task="sweep_floor", seed=42)
policy = HeuristicPolicy()
metrics = VICMetrics()

obs = env.reset()
done = False
while not done:
    action = policy.act(obs)
    obs, reward, done, info = env.step(action)
    metrics.update(info)

print(metrics.summary())  # TCR, SE, MQ, CP, DA
```

CLI:

```
vic-eval --vehicle sedan --task sweep_floor --policy heuristic --episodes 20
```

## Invariants
- The `vic` package import succeeds on machines without Isaac Sim. Sim-only symbols raise `ImportError` only when invoked.
- All metrics are computable from the standardized `info` dict — no hidden global state.
- Configs (`configs/vehicles.yaml`, `configs/tasks.yaml`) are the source of truth for vehicle classes, clutter classes, and task parameters.
- Random seeds are reproducible: `VICEnv(seed=42).reset()` returns the same initial state across runs.
- No vehicle assets ship with this repo. Procedural primitive-mesh generators stand in until real assets are imported (which would need its own ADR for asset licensing).

## Things that look broken but aren't
- The Isaac Sim imports inside `env.py` are wrapped in try/except. This is **deliberate**, not lazy — it lets `pytest tests/` run on macOS without Isaac installed, validating the pure-Python parts (metrics, configs, task definitions) for fast iteration.
- `pyproject.toml` does **not** include `isaaclab` as a hard dependency. This is deliberate: requiring Isaac Lab to install the package would make development on non-Linux/non-RTX machines impossible. Use `pip install -e ".[isaac]"` to opt in.
- The heuristic baseline does not call into Isaac Sim. It produces actions purely from the standardized observation dict, so it can be unit-tested without the simulator.
- `metrics.py` computes Damage Avoidance (DA) by counting `info["collisions"]` events with `parts in {"seat", "dashboard", "mirror", "windshield"}`. Empty-list inputs return `da=1.0` (perfect), not an error — by convention.

## Linked ADRs
- ADR-0005 — VIC benchmark scope + Isaac Sim selection (the primary ADR for this module)
- ADR-0001 — Markdown is the data layer (SPEC.md is markdown; configs are YAML)
- ADR-0002 — Append-only governance (this MODULE.md is part of the cache cold context)

## Roadmap
The scaffold is v0.1. Sequential follow-ups, each its own Tier 1 or Tier 2 charter:
- v0.2 — Provision Isaac Sim host, validate end-to-end rollout on a real episode
- v0.3 — Procedural vehicle interior generator (3 classes × N variations)
- v0.4 — Map-based planner baseline (matches CleanUpBench's second baseline)
- v0.5 — Headless eval CLI for CI; metric serialization to JSON
- v1.0 — Released benchmark with leaderboard format spec

## Out of scope
- Trained RL policies (separate Tier 2 ADR when ready)
- Real vehicle CAD/USD assets (asset licensing is its own irreversible decision)
- Sim-to-real transfer
- Vision-language policies
- Multi-robot coordination

## How to read this module
1. Start with [`SPEC.md`](./SPEC.md) for the formal task and metric definitions.
2. [`README.md`](./README.md) has the install steps and quickstart.
3. [`src/vic/`](./src/vic/) is the implementation; entry point is `eval.py`.
4. [`tests/`](./tests/) covers what runs without Isaac Sim.
