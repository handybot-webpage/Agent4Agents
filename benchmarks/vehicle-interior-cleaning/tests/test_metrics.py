"""Tests for vic.metrics — pure-Python, no Isaac required."""

from __future__ import annotations

import pytest

from vic.metrics import VICMetrics, aggregate, DAMAGE_FORCE_THRESHOLD_N


def test_empty_metrics_perfect_scores():
    """No data = perfect (1.0) on every metric except CP which depends on time."""
    m = VICMetrics(max_episode_seconds=300.0)
    s = m.summary()
    assert s["tcr"] == 1.0   # no items present, no failure
    assert s["se"] == 1.0    # no sweeping, no penalty
    assert s["mq"] == 1.0    # no jerk samples
    assert s["cp"] == 1.0    # no time elapsed
    assert s["da"] == 1.0    # no damage collisions
    assert s["vic"] == 1.0


def test_tcr_partial_completion():
    m = VICMetrics(max_episode_seconds=300.0)
    m.update({"items_present": 50, "items_resolved": 30})
    assert m.tcr() == pytest.approx(0.6)


def test_tcr_overshoot_clipped_to_one():
    m = VICMetrics(max_episode_seconds=300.0)
    m.update({"items_present": 10, "items_resolved": 100})
    assert m.tcr() == 1.0


def test_se_with_no_redundancy():
    m = VICMetrics(max_episode_seconds=300.0)
    m.update({"swept_area_m2": 5.0, "redundant_swept_area_m2": 0.0})
    assert m.se() == 1.0


def test_se_full_redundancy():
    m = VICMetrics(max_episode_seconds=300.0)
    m.update({"swept_area_m2": 5.0, "redundant_swept_area_m2": 5.0})
    assert m.se() == 0.0


def test_mq_smooth_motion_high_score():
    m = VICMetrics(max_episode_seconds=300.0)
    for _ in range(10):
        m.update({"joint_jerk": 0.5})  # very smooth
    assert m.mq() > 0.95


def test_mq_jerky_motion_low_score():
    m = VICMetrics(max_episode_seconds=300.0)
    for _ in range(10):
        m.update({"joint_jerk": 500.0})  # very jerky
    assert m.mq() < 0.05


def test_cp_full_time_used():
    m = VICMetrics(max_episode_seconds=300.0)
    m.update({"dt": 300.0})
    assert m.cp() == 0.0


def test_cp_quick_finish():
    m = VICMetrics(max_episode_seconds=300.0)
    m.update({"dt": 30.0})
    assert m.cp() == pytest.approx(0.9)


def test_da_damage_collisions_count_only_above_threshold():
    m = VICMetrics(max_episode_seconds=300.0)
    # below threshold — does not count
    m.update({"collisions": [{"part": "seat", "force_n": DAMAGE_FORCE_THRESHOLD_N - 0.1}]})
    assert m.damage_collisions == 0
    # above threshold — counts
    m.update({"collisions": [{"part": "dashboard", "force_n": DAMAGE_FORCE_THRESHOLD_N + 5.0}]})
    assert m.damage_collisions == 1
    # non-fragile part — does not count even above threshold
    m.update({"collisions": [{"part": "floor_mat", "force_n": 100.0}]})
    assert m.damage_collisions == 1


def test_da_max_damage_zeros_score():
    m = VICMetrics(max_episode_seconds=300.0)
    for _ in range(10):
        m.update({"collisions": [{"part": "windshield", "force_n": 50.0}]})
    assert m.da() == 0.0


def test_aggregate_mean_std():
    m1 = VICMetrics(max_episode_seconds=300.0)
    m1.update({"items_present": 10, "items_resolved": 10})
    m2 = VICMetrics(max_episode_seconds=300.0)
    m2.update({"items_present": 10, "items_resolved": 0})
    agg = aggregate([m1, m2])
    assert agg["tcr"]["mean"] == pytest.approx(0.5)
    assert agg["tcr"]["std"] == pytest.approx(0.5)
    assert agg["tcr"]["n"] == 2


def test_summary_contains_vic_composite():
    m = VICMetrics(max_episode_seconds=300.0)
    m.update({"items_present": 10, "items_resolved": 5})
    s = m.summary()
    assert "vic" in s
    expected_composite = sum([s["tcr"], s["se"], s["mq"], s["cp"], s["da"]]) / 5
    assert s["vic"] == pytest.approx(expected_composite)
