"""Tests for vic.config + vic.tasks — config loaders and task dataclass."""

from __future__ import annotations

import pytest

from vic.config import (
    load_vehicles,
    load_tasks,
    load_clutter,
    vehicle_classes,
    task_names,
    clutter_classes,
)
from vic.tasks import VICTask


def test_three_vehicle_classes_present():
    classes = vehicle_classes()
    assert set(classes) == {"sedan", "suv", "hatchback"}


def test_four_tasks_present():
    tasks = task_names()
    assert set(tasks) == {"sweep_floor", "pickup_objects", "spot_clean_seat", "full_clean"}


def test_four_clutter_classes_present():
    classes = clutter_classes()
    assert set(classes) == {
        "small_debris", "medium_object", "fabric_dust", "liquid_spill",
    }


def test_vehicle_config_has_required_fields():
    for name, spec in load_vehicles().items():
        for field in ("cabin_volume_m3", "cabin_dims_m", "seats_per_row", "fragile_parts"):
            assert field in spec, f"{name} missing {field!r}"
        # fragile_parts must include the SPEC.md damage parts
        assert "windshield" in spec["fragile_parts"]


def test_task_config_has_required_fields():
    for name, spec in load_tasks().items():
        for field in ("episode_seconds", "termination", "metrics_weight"):
            assert field in spec, f"{name} missing {field!r}"
        # metric weights must reference the five SPEC metrics
        for metric in ("tcr", "se", "mq", "cp", "da"):
            assert metric in spec["metrics_weight"], f"{name} missing weight for {metric!r}"


def test_clutter_config_has_required_fields():
    for name, spec in load_clutter().items():
        assert "interaction_mode" in spec
        assert spec["interaction_mode"] in ("sweep", "grasp", "spot_clean")


def test_vic_task_from_config_round_trip():
    t = VICTask.from_config("sweep_floor")
    assert t.name == "sweep_floor"
    assert t.episode_seconds == 300
    assert "small_debris" in t.clutter
    assert "floor_front" in t.placement_zones


def test_vic_task_unknown_name_raises():
    with pytest.raises(KeyError):
        VICTask.from_config("nonexistent_task")


def test_vic_task_composite_score_uses_weights():
    t = VICTask.from_config("sweep_floor")
    # All-perfect per-metric scores
    perfect = {"tcr": 1.0, "se": 1.0, "mq": 1.0, "cp": 1.0, "da": 1.0}
    assert t.composite_score(perfect) == pytest.approx(1.0)
    # Zero TCR with sweep_floor's TCR weight 0.4
    only_tcr_zero = {"tcr": 0.0, "se": 1.0, "mq": 1.0, "cp": 1.0, "da": 1.0}
    score = t.composite_score(only_tcr_zero)
    weight_sum = sum(t.metrics_weight.values())
    expected = (1.0 - t.metrics_weight["tcr"]) / weight_sum * weight_sum / weight_sum  # = 1 - 0.4 normalized
    assert score == pytest.approx(1.0 - t.metrics_weight["tcr"] / weight_sum)
