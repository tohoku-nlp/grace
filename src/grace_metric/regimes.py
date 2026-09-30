"""Representative GRACE regimes and a convenience all-metrics helper.

The three regimes are the calibrated presets from the paper (Table I),
spanning permissive household-style evaluation to strict
disaster/medical-style deadlines.
"""

from .core import grace
from .baselines import sr_only, sr_over_time, weighted_sum, spl

__all__ = ["REGIMES", "compute_all_metrics"]

#: Calibrated ``(beta, tau)`` presets spanning permissive to strict deadlines.
REGIMES = {
    "permissive": {"beta": 1.0, "tau": 0.0},   # e.g. household tasks
    "moderate":   {"beta": 1.0, "tau": 0.43},  # e.g. warehouse logistics
    "strict":     {"beta": 2.0, "tau": 5.67},  # e.g. disaster / medical
}


def compute_all_metrics(A: float, r: float) -> dict:
    """Compute GRACE (all regimes) and every baseline for one ``(A, r)`` pair.

    Args:
        A: Success rate in ``[0, 1]``.
        r: Normalized runtime, ``r >= 0``.

    Returns:
        Dict mapping metric name to score.
    """
    results = {
        "SR": sr_only(A, r),
        "SR/Time": sr_over_time(A, r),
        "WSum_0.3": weighted_sum(A, r, alpha=0.3),
        "WSum_0.5": weighted_sum(A, r, alpha=0.5),
        "WSum_0.7": weighted_sum(A, r, alpha=0.7),
        "SPL": spl(A, r),
    }
    for name, params in REGIMES.items():
        results[f"GRACE_{name}"] = grace(A, r, **params)
    return results
