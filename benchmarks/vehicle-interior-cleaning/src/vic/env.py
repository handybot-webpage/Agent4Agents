"""VIC environment wrapper around Isaac Lab's ManagerBasedRLEnv.

Isaac Sim is Linux + NVIDIA RTX only (per ADR-0005). This module is structured
so that *importing* `vic.env` succeeds on any platform — but instantiating
`VICEnv` raises a clear ImportError if Isaac Lab is not present, with a
pointer to the platform docs.

This separation lets `import vic` work for unit tests on macOS while keeping
the full env available on the real deploy target.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from typing import Any

from .config import load_vehicles
from .tasks import VICTask


def _isaac_available() -> bool:
    """True iff isaaclab is importable in the current process."""
    return importlib.util.find_spec("isaaclab") is not None


_ISAAC_INSTALL_HINT = (
    "Isaac Lab is required for the VIC environment runtime.\n"
    "Platform requirements: Linux x86_64 + NVIDIA RTX GPU (per ADR-0005).\n"
    "Install: see benchmarks/vehicle-interior-cleaning/README.md "
    "'Install — host with Isaac Sim'."
)


@dataclass
class _VICObservation:
    """Standardized observation shape (subset documented for baseline use)."""
    phase: str
    robot_pose: tuple[float, float, float]
    clutter_visible: list[dict[str, Any]]
    spills_visible: list[dict[str, Any]]
    bin_pose: tuple[float, float, float]
    holding: str | None = None


class VICEnv:
    """Vehicle Interior Cleaning environment.

    Constructor raises ImportError if Isaac Lab isn't installed. This is
    deliberate: it keeps the rest of the package usable for development and
    testing on machines without the simulator (per ADR-0005).
    """

    def __init__(
        self,
        vehicle_class: str = "sedan",
        task: str | VICTask = "sweep_floor",
        seed: int = 0,
        headless: bool = True,
    ):
        if not _isaac_available():
            raise ImportError(_ISAAC_INSTALL_HINT)

        # Defer Isaac imports so the module loads on machines without Isaac
        from isaaclab.envs import ManagerBasedRLEnv  # noqa: F401  (real impl uses this)

        vehicles = load_vehicles()
        if vehicle_class not in vehicles:
            raise ValueError(
                f"unknown vehicle_class {vehicle_class!r}; "
                f"available: {list(vehicles.keys())}"
            )

        self.vehicle_class = vehicle_class
        self.vehicle_cfg = vehicles[vehicle_class]
        self.task = task if isinstance(task, VICTask) else VICTask.from_config(task)
        self.seed = seed
        self.headless = headless

        # The Isaac Lab env initialization happens here. Concrete construction
        # of the ManagerBasedRLEnv with USD scene, task config, and reward terms
        # is intentionally not implemented in v0.1 — it requires the real Isaac
        # host to develop against. Stub raises NotImplementedError if reached.
        raise NotImplementedError(
            "VICEnv runtime is a v0.1 stub. The init signature, vehicle/task "
            "validation, and observation/action contracts are defined here, but "
            "scene assembly with Isaac Lab is deferred to v0.2 (Provision Isaac "
            "Sim host) per benchmarks/vehicle-interior-cleaning/MODULE.md."
        )

    # The following methods are part of the public contract but are not callable
    # in v0.1 because the constructor raises before reaching them. They are
    # retained as documentation of the intended Gymnasium-style interface.

    def reset(self) -> dict[str, Any]:
        raise NotImplementedError("VICEnv.reset — v0.2")

    def step(self, action: dict[str, Any]) -> tuple[dict[str, Any], float, bool, dict[str, Any]]:
        raise NotImplementedError("VICEnv.step — v0.2")

    def close(self) -> None:
        raise NotImplementedError("VICEnv.close — v0.2")
