"""Tests for the GRACE metric and baselines."""

import math

import pytest

from grace_metric import (
    grace,
    t_star,
    weights_to_params,
    sr_only,
    sr_over_time,
    weighted_sum,
    spl,
    REGIMES,
    compute_all_metrics,
)


# --- t_star ---

def test_t_star_at_zero_is_one():
    assert t_star(0.0, tau=0.0) == 1.0


def test_t_star_decreasing_in_r():
    vals = [t_star(r, tau=0.0) for r in [0.0, 0.5, 1.0, 2.0, 4.0]]
    assert all(a > b for a, b in zip(vals, vals[1:]))


def test_t_star_tau_only_penalizes_overrun():
    # For r <= 1 the exp term is 1 regardless of tau.
    assert t_star(0.8, tau=0.0) == pytest.approx(t_star(0.8, tau=10.0))
    # For r > 1 a larger tau strictly lowers the score.
    assert t_star(2.0, tau=5.0) < t_star(2.0, tau=0.0)


# --- grace core properties ---

def test_grace_in_unit_interval():
    for A in [0.0, 0.3, 1.0]:
        for r in [0.0, 0.5, 1.0, 3.0]:
            s = grace(A, r, beta=1.0, tau=0.43)
            assert 0.0 <= s <= 1.0


def test_grace_zero_accuracy_is_zero():
    assert grace(0.0, 0.5) == 0.0


def test_grace_perfect_is_one():
    # A = 1 and r = 0 (instant, perfect) -> T* = 1 -> harmonic mean 1.
    assert grace(1.0, 0.0, beta=1.0, tau=0.0) == pytest.approx(1.0)


def test_grace_is_harmonic_mean_at_beta_one():
    A, r = 0.6, 0.7
    Ts = t_star(r, tau=0.0)
    expected = 2 * A * Ts / (A + Ts)
    assert grace(A, r, beta=1.0, tau=0.0) == pytest.approx(expected)


def test_grace_beta_shifts_toward_speed():
    # F-beta convention: larger beta emphasizes the speed term T*.
    # When accuracy is low but the agent is fast (high T*), larger beta
    # should raise the score toward T*.
    A, r = 0.3, 0.2  # low accuracy, fast -> T* near 1
    assert grace(A, r, beta=3.0, tau=0.0) > grace(A, r, beta=1.0, tau=0.0)
    # Conversely, with high accuracy but slow runtime, larger beta lowers it.
    assert grace(0.9, 2.0, beta=3.0) < grace(0.9, 2.0, beta=1.0)


def test_grace_degenerate_denominator():
    # A = 0 and r large -> both terms ~0; must not raise.
    assert grace(0.0, 1e9, beta=0.0, tau=0.0) == 0.0


# --- weights_to_params ---

def test_weights_to_params_midpoint():
    beta, tau = weights_to_params(0.5, 0.0)
    assert beta == pytest.approx(1.0)
    assert tau == pytest.approx(0.0)


def test_weights_to_params_monotonic():
    b_lo, _ = weights_to_params(0.3, 0.5)
    b_hi, _ = weights_to_params(0.7, 0.5)
    assert b_hi > b_lo


# --- baselines ---

def test_sr_only_ignores_runtime():
    assert sr_only(0.5, 0.1) == sr_only(0.5, 100.0) == 0.5


def test_sr_over_time():
    assert sr_over_time(0.8, 2.0) == pytest.approx(0.4)
    assert sr_over_time(0.8, 0.0) == 0.8  # guard for r <= 0


def test_weighted_sum_caps_efficiency():
    # r < 1 -> 1/r > 1, capped at 1.
    assert weighted_sum(1.0, 0.5, alpha=0.5) == pytest.approx(1.0)


def test_spl_matches_formula():
    assert spl(0.6, 2.0) == pytest.approx(0.3)


# --- regimes ---

def test_regimes_keys():
    assert set(REGIMES) == {"permissive", "moderate", "strict"}


def test_compute_all_metrics_keys():
    out = compute_all_metrics(0.7, 1.2)
    for key in ["SR", "SR/Time", "WSum_0.5", "SPL",
                "GRACE_permissive", "GRACE_moderate", "GRACE_strict"]:
        assert key in out
    assert all(isinstance(v, float) for v in out.values())
