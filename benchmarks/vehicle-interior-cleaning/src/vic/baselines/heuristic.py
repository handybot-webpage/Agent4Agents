"""Heuristic baseline policy.

Three-phase scripted policy:
  1. raster-sweep the floor for small_debris + fabric_dust
  2. greedy-nearest grasp of medium_objects, deposit in bin
  3. for each detected liquid_spill centroid: navigate end-effector,
     execute a circular wipe motion

Pure Python — no Isaac dependency. Operates on a standardized observation
dict, so it can be exercised by unit tests with synthetic obs and on Isaac
Sim alike.

Observation contract (subset, see env.py for full spec):
    obs["phase"]              str   — current task phase ("sweep"/"grasp"/"wipe")
    obs["robot_pose"]         tuple — (x, y, yaw) base pose
    obs["clutter_visible"]    list  — [{"id": str, "class": str, "centroid": (x, y, z)}]
    obs["bin_pose"]           tuple — (x, y, z) deposit location
    obs["spills_visible"]     list  — [{"id": str, "centroid": (x, y, z), "coverage": float}]

Action contract:
    action = {
        "kind": one of {"sweep_to", "grasp_at", "place_at", "wipe_at", "noop"},
        "target": (x, y, z) or (x, y) depending on kind,
        "force_n": float (only for "wipe_at"),
    }
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class HeuristicPolicy:
    """Scripted three-phase cleaning policy."""

    wipe_force_n: float = 5.0
    sweep_step_m: float = 0.2
    _phase_state: str = "sweep"

    def reset(self) -> None:
        self._phase_state = "sweep"

    def act(self, obs: dict[str, Any]) -> dict[str, Any]:
        """Return next action given observation."""
        # Phase transitions follow obs["phase"] if present; otherwise our local state
        phase = obs.get("phase", self._phase_state)

        if phase in ("sweep", "sweep_floor"):
            return self._act_sweep(obs)
        if phase in ("grasp", "pickup_objects"):
            return self._act_grasp(obs)
        if phase in ("wipe", "spot_clean_seat"):
            return self._act_wipe(obs)
        return {"kind": "noop"}

    def _act_sweep(self, obs: dict[str, Any]) -> dict[str, Any]:
        debris = [
            c for c in obs.get("clutter_visible", [])
            if c.get("class") in ("small_debris", "fabric_dust")
        ]
        if not debris:
            self._phase_state = "grasp"
            return {"kind": "noop"}
        target = self._nearest(obs.get("robot_pose", (0.0, 0.0, 0.0)), debris)
        return {"kind": "sweep_to", "target": tuple(target["centroid"][:2])}

    def _act_grasp(self, obs: dict[str, Any]) -> dict[str, Any]:
        objects = [
            c for c in obs.get("clutter_visible", [])
            if c.get("class") == "medium_object"
        ]
        if not objects:
            self._phase_state = "wipe"
            return {"kind": "noop"}
        target = self._nearest(obs.get("robot_pose", (0.0, 0.0, 0.0)), objects)
        # Two-action sequence: grasp, then place. Heuristic picks grasp first
        # and lets caller invoke place via subsequent step. For simplicity we
        # emit grasp_at; the env is expected to track held object.
        if obs.get("holding"):
            bin_pose = obs.get("bin_pose", (0.0, 0.0, 0.0))
            return {"kind": "place_at", "target": tuple(bin_pose)}
        return {"kind": "grasp_at", "target": tuple(target["centroid"])}

    def _act_wipe(self, obs: dict[str, Any]) -> dict[str, Any]:
        spills = obs.get("spills_visible", [])
        if not spills:
            self._phase_state = "done"
            return {"kind": "noop"}
        # Wipe the spill with highest current coverage (most stained first)
        target = max(spills, key=lambda s: s.get("coverage", 0.0))
        return {
            "kind": "wipe_at",
            "target": tuple(target["centroid"]),
            "force_n": self.wipe_force_n,
        }

    @staticmethod
    def _nearest(pose: tuple[float, float, float],
                 candidates: list[dict[str, Any]]) -> dict[str, Any]:
        rx, ry = pose[0], pose[1]
        return min(
            candidates,
            key=lambda c: (c["centroid"][0] - rx) ** 2 + (c["centroid"][1] - ry) ** 2,
        )
