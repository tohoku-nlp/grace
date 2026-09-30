"""Baseline metrics used for comparison in the GRACE paper.

These reproduce the alternatives GRACE is compared against: success-rate-only,
success-over-time, weighted sum at various mixing weights, and an SPL-style
score. All are pure-Python and dependency-free.
"""

from .core import _check

__all__ = ["sr_only", "sr_over_time", "weighted_sum", "spl"]


def sr_only(A: float, r: float = 0.0) -> float:
    """Success rate only (ignores runtime). ``r`` is accepted but unused."""
    return _check("A", A, high=1.0)


def sr_over_time(A: float, r: float) -> float:
    """Success rate divided by normalized runtime, ``A / r``.

    Returns ``A`` when ``r == 0`` (no time elapsed). Unlike the other metrics
    here, this ratio is **not** bounded by ``1``: a fast agent (``r < A``)
    scores above one. It is included to reproduce the paper's comparison, not
    as a normalized score.

    Raises:
        ValueError: if ``A`` is outside ``[0, 1]`` or ``r`` is negative,
            ``nan``, or ``inf``.
    """
    A = _check("A", A, high=1.0)
    r = _check("r", r)
    if r == 0:
        return A
    return A / r


def weighted_sum(A: float, r: float, alpha: float = 0.5) -> float:
    """Convex combination of accuracy and a capped speed term.

    ``alpha * A + (1 - alpha) * min(1, 1 / r)``.

    Args:
        A: Success rate in ``[0, 1]``.
        r: Normalized runtime, ``r >= 0``.
        alpha: Weight on accuracy in ``[0, 1]``.

    Raises:
        ValueError: if any argument is out of range, ``nan``, or ``inf``.
    """
    A = _check("A", A, high=1.0)
    r = _check("r", r)
    alpha = _check("alpha", alpha, high=1.0)
    efficiency = min(1.0 / r, 1.0) if r > 0 else 1.0
    return alpha * A + (1.0 - alpha) * efficiency


def spl(A: float, r: float) -> float:
    """SPL-style metric ``SR * min(1, 1 / r)``.

    Mirrors Success weighted by Path Length with normalized runtime as a
    proxy for the path-length ratio (capped at 1).

    Raises:
        ValueError: if ``A`` is outside ``[0, 1]`` or ``r`` is negative,
            ``nan``, or ``inf``.
    """
    A = _check("A", A, high=1.0)
    r = _check("r", r)
    efficiency = min(1.0, 1.0 / r) if r > 0 else 1.0
    return A * efficiency
