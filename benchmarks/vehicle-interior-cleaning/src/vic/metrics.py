"""VIC benchmark metrics: TCR, SE, MQ, CP, DA.

All metrics are computable from a stream of standardized `info` dicts emitted
by the env on each step. This separation is deliberate: the metrics module
has no Isaac dependency and can be unit-tested on any platform.

See SPEC.md §5 for definitions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import exp
from typing import Iterable, Sequence

# Default fragile-part set per SPEC.md §5.5
DAMAGE_PARTS: frozenset[str] = frozenset({
    "seat", "dashboard", "mirror", "windshield", "steering_wheel",
})
DAMAGE_FORCE_THRESHOLD_N = 5.0
DAMAGE_MAX_ALLOWED = 5
JERK_DECAY_K = 50.0  # tunable per SPEC.md §5.3


@dataclass
class VICMetrics:
    """Incrementally aggregates per-step info dicts; exposes scores at end."""

    items_present: int = 0
    items_resolved: int = 0
    swept_area_m2: float = 0.0
    redundant_swept_area_m2: float = 0.0
    joint_jerks: list[float] = field(default_factory=list)
    damage_collisions: int = 0
    elapsed_seconds: float = 0.0
    max_episode_seconds: float = 1.0

    @classmethod
    def for_task(cls, task) -> "VICMetrics":
        """Initialize with task-specific max_episode_seconds."""
        return cls(max_episode_seconds=float(task.episode_seconds))

    def update(self, info: dict) -> None:
        """Consume one step's info dict.

        Expected keys (all optional; absent keys produce no update):
            items_present, items_resolved (int) — counts at this step
            swept_area_m2, redundant_swept_area_m2 (float) — running totals
            joint_jerk (float) — instantaneous joint-jerk magnitude
            collisions (list[dict]) — each: {part: str, force_n: float}
            dt (float) — elapsed seconds at this step
        """
        if "items_present" in info:
            self.items_present = int(info["items_present"])
        if "items_resolved" in info:
            self.items_resolved = int(info["items_resolved"])
        if "swept_area_m2" in info:
            self.swept_area_m2 = float(info["swept_area_m2"])
        if "redundant_swept_area_m2" in info:
            self.redundant_swept_area_m2 = float(info["redundant_swept_area_m2"])
        if "joint_jerk" in info:
            self.joint_jerks.append(float(info["joint_jerk"]))
        for col in info.get("collisions", []):
            if (col.get("part") in DAMAGE_PARTS
                    and float(col.get("force_n", 0.0)) > DAMAGE_FORCE_THRESHOLD_N):
                self.damage_collisions += 1
        if "dt" in info:
            self.elapsed_seconds += float(info["dt"])

    # ---- per-metric scores in [0, 1] ----

    def tcr(self) -> float:
        if self.items_present <= 0:
            return 1.0
        return max(0.0, min(1.0, self.items_resolved / self.items_present))

    def se(self) -> float:
        if self.swept_area_m2 <= 0:
            return 1.0  # nothing to sweep, no penalty
        ratio = self.redundant_swept_area_m2 / self.swept_area_m2
        return max(0.0, min(1.0, 1.0 - ratio))

    def mq(self) -> float:
        if not self.joint_jerks:
            return 1.0
        mean_jerk = sum(self.joint_jerks) / len(self.joint_jerks)
        return max(0.0, min(1.0, exp(-mean_jerk / JERK_DECAY_K)))

    def cp(self) -> float:
        if self.max_episode_seconds <= 0:
            return 0.0
        return max(0.0, min(1.0, 1.0 - (self.elapsed_seconds / self.max_episode_seconds)))

    def da(self) -> float:
        return max(0.0, min(1.0, 1.0 - (self.damage_collisions / DAMAGE_MAX_ALLOWED)))

    def per_metric(self) -> dict[str, float]:
        return {
            "tcr": self.tcr(),
            "se": self.se(),
            "mq": self.mq(),
            "cp": self.cp(),
            "da": self.da(),
        }

    def composite(self) -> float:
        """Unweighted mean of the five per-metric scores (VIC composite)."""
        scores = self.per_metric().values()
        return sum(scores) / len(scores)

    def summary(self) -> dict[str, float]:
        out = self.per_metric()
        out["vic"] = self.composite()
        return out


def aggregate(metrics_list: Sequence[VICMetrics]) -> dict[str, dict[str, float]]:
    """Aggregate a list of per-episode metrics into mean/std per metric."""
    if not metrics_list:
        return {}
    keys = ("tcr", "se", "mq", "cp", "da", "vic")
    summaries = [m.summary() for m in metrics_list]
    n = len(summaries)
    out: dict[str, dict[str, float]] = {}
    for k in keys:
        vals = [s[k] for s in summaries]
        mean = sum(vals) / n
        var = sum((v - mean) ** 2 for v in vals) / n
        out[k] = {"mean": mean, "std": var ** 0.5, "n": n}
    return out
