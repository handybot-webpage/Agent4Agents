"""Tests for the heuristic baseline policy on synthetic observations."""

from __future__ import annotations

import pytest

from vic.baselines.heuristic import HeuristicPolicy


def _obs(phase, **overrides):
    base = {
        "phase": phase,
        "robot_pose": (0.0, 0.0, 0.0),
        "clutter_visible": [],
        "spills_visible": [],
        "bin_pose": (0.0, 0.0, 0.0),
        "holding": None,
    }
    base.update(overrides)
    return base


def test_sweep_phase_targets_nearest_debris():
    p = HeuristicPolicy()
    obs = _obs(
        "sweep",
        clutter_visible=[
            {"id": "d1", "class": "small_debris", "centroid": (5.0, 0.0, 0.0)},
            {"id": "d2", "class": "small_debris", "centroid": (1.0, 0.0, 0.0)},
            {"id": "d3", "class": "small_debris", "centroid": (10.0, 0.0, 0.0)},
        ],
    )
    a = p.act(obs)
    assert a["kind"] == "sweep_to"
    assert a["target"] == (1.0, 0.0)


def test_sweep_phase_ignores_medium_objects():
    p = HeuristicPolicy()
    obs = _obs(
        "sweep",
        clutter_visible=[
            {"id": "m1", "class": "medium_object", "centroid": (1.0, 0.0, 0.0)},
        ],
    )
    a = p.act(obs)
    # No debris, so policy emits noop and advances internal phase
    assert a["kind"] == "noop"


def test_grasp_phase_picks_nearest_object_when_empty_handed():
    p = HeuristicPolicy()
    obs = _obs(
        "grasp",
        clutter_visible=[
            {"id": "m1", "class": "medium_object", "centroid": (3.0, 0.0, 0.0)},
            {"id": "m2", "class": "medium_object", "centroid": (1.0, 1.0, 0.0)},
        ],
    )
    a = p.act(obs)
    assert a["kind"] == "grasp_at"
    assert a["target"] == (1.0, 1.0, 0.0)


def test_grasp_phase_places_when_holding_object():
    p = HeuristicPolicy()
    obs = _obs(
        "grasp",
        holding="m1",
        bin_pose=(0.0, -2.0, 0.5),
        clutter_visible=[
            {"id": "m2", "class": "medium_object", "centroid": (3.0, 0.0, 0.0)},
        ],
    )
    a = p.act(obs)
    assert a["kind"] == "place_at"
    assert a["target"] == (0.0, -2.0, 0.5)


def test_wipe_phase_targets_highest_coverage_spill():
    p = HeuristicPolicy()
    obs = _obs(
        "wipe",
        spills_visible=[
            {"id": "s1", "centroid": (1.0, 0.0, 0.5), "coverage": 0.3},
            {"id": "s2", "centroid": (5.0, 0.0, 0.5), "coverage": 0.8},
            {"id": "s3", "centroid": (3.0, 0.0, 0.5), "coverage": 0.5},
        ],
    )
    a = p.act(obs)
    assert a["kind"] == "wipe_at"
    assert a["target"] == (5.0, 0.0, 0.5)
    assert a["force_n"] == pytest.approx(5.0)


def test_unknown_phase_returns_noop():
    p = HeuristicPolicy()
    a = p.act(_obs("unknown_phase"))
    assert a["kind"] == "noop"


def test_reset_returns_policy_to_sweep():
    p = HeuristicPolicy()
    p._phase_state = "wipe"
    p.reset()
    assert p._phase_state == "sweep"
