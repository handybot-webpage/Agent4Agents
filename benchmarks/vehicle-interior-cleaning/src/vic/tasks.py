"""Task specifications loaded from configs/tasks.yaml.

A VICTask is a frozen dataclass capturing everything an env needs to set up
a particular cleaning challenge.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .config import load_tasks


@dataclass(frozen=True)
class VICTask:
    name: str
    episode_seconds: int
    clutter: dict[str, dict[str, int]]
    placement_zones: tuple[str, ...]
    termination: tuple[str, ...]
    metrics_weight: dict[str, float]
    description: str = ""
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_config(cls, name: str) -> "VICTask":
        cfg = load_tasks()
        if name not in cfg:
            raise KeyError(f"unknown task {name!r}; available: {list(cfg.keys())}")
        spec = cfg[name]
        # Pull recognized fields; everything else into `extra`
        recognized = {
            "episode_seconds", "clutter", "placement_zones", "termination",
            "metrics_weight", "description",
        }
        extra = {k: v for k, v in spec.items() if k not in recognized}
        return cls(
            name=name,
            episode_seconds=int(spec["episode_seconds"]),
            clutter=spec.get("clutter", {}),
            placement_zones=tuple(spec.get("placement_zones", ())),
            termination=tuple(spec.get("termination", ())),
            metrics_weight=dict(spec.get("metrics_weight", {})),
            description=spec.get("description", ""),
            extra=extra,
        )

    def composite_score(self, per_metric: dict[str, float]) -> float:
        """Weighted composite score from per-metric scores using metrics_weight."""
        total = 0.0
        weight_sum = 0.0
        for metric, weight in self.metrics_weight.items():
            if metric in per_metric:
                total += per_metric[metric] * weight
                weight_sum += weight
        if weight_sum <= 0:
            return 0.0
        return total / weight_sum
