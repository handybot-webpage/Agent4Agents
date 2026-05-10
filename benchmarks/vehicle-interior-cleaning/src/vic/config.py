"""Config loaders for vehicles, tasks, and clutter classes.

YAML is the source of truth (per ADR-0001 — Markdown/YAML data layer).
Returns plain dicts; callers wrap into dataclasses if they want types.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def _configs_dir() -> Path:
    """Resolve `configs/` relative to this file (works for installed + editable)."""
    return Path(__file__).resolve().parent.parent.parent / "configs"


def _load_yaml(filename: str) -> dict[str, Any]:
    path = _configs_dir() / filename
    if not path.is_file():
        raise FileNotFoundError(f"config not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"config root must be a mapping, got {type(data).__name__}: {path}")
    return data


def load_vehicles() -> dict[str, dict[str, Any]]:
    """Return the `vehicles` mapping: class_name -> config."""
    return _load_yaml("vehicles.yaml")["vehicles"]


def load_tasks() -> dict[str, dict[str, Any]]:
    """Return the `tasks` mapping: task_name -> config."""
    return _load_yaml("tasks.yaml")["tasks"]


def load_clutter() -> dict[str, dict[str, Any]]:
    """Return the `clutter_classes` mapping: clutter_name -> config."""
    return _load_yaml("clutter.yaml")["clutter_classes"]


def vehicle_classes() -> list[str]:
    return list(load_vehicles().keys())


def task_names() -> list[str]:
    return list(load_tasks().keys())


def clutter_classes() -> list[str]:
    return list(load_clutter().keys())
