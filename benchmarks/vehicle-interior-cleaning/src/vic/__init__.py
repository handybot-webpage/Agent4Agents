"""Vehicle Interior Cleaning (VIC) Benchmark.

Paper-inspired by CleanUpBench (arxiv 2508.05543), domain-shifted to vehicle
interiors. Built on NVIDIA Isaac Sim per ADR-0005.

Public API:
    VICEnv          — environment wrapper (requires Isaac Sim at runtime)
    VICTask         — task spec dataclass
    VICMetrics      — incremental metric aggregator
    HeuristicPolicy — scripted baseline (no Isaac required)
    load_vehicles, load_tasks, load_clutter — config loaders

The env import is intentionally lazy: the Python package imports cleanly on
machines without Isaac Sim. Sim-dependent symbols raise a clear ImportError
only when actually invoked.
"""

from .config import load_vehicles, load_tasks, load_clutter
from .tasks import VICTask
from .metrics import VICMetrics
from .baselines.heuristic import HeuristicPolicy

__version__ = "0.1.0"

__all__ = [
    "VICTask",
    "VICMetrics",
    "HeuristicPolicy",
    "load_vehicles",
    "load_tasks",
    "load_clutter",
    "VICEnv",  # lazy
]


def __getattr__(name):
    """Lazy import of Isaac-Sim-dependent symbols."""
    if name == "VICEnv":
        from .env import VICEnv
        return VICEnv
    raise AttributeError(f"module 'vic' has no attribute {name!r}")
