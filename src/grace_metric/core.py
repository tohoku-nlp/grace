"""Core GRACE metric.

GRACE (Generalized Robotics Accuracy-Completion Evaluation) is a tunable
harmonic-mean score that unifies task accuracy and time efficiency:

    GRACE(A, r; beta, tau) = (1 + beta^2) * A * T*(r) / (beta^2 * A + T*(r))

with the normalized real-time ability

    T*(r) = 1 / (1 + r^2) * exp(-tau * max(0, r - 1)).

Both functions are pure-Python and dependency-free.
"""

import math

__all__ = ["t_star", "grace", "weights_to_params"]


def _check(name: str, value: float, *, low: float = 0.0,
           high: float = math.inf, low_open: bool = False,
           high_open: bool = False) -> float:
    """Validate that ``value`` is a finite number in the required range.

    Raises ``TypeError`` for non-numeric input and ``ValueError`` for
    ``nan``/``inf`` or out-of-range values.
    """
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a real number, got {type(value).__name__}")
    v = float(value)
    if not math.isfinite(v):
        raise ValueError(f"{name} must be finite, got {value!r}")
    lo_ok = v > low if low_open else v >= low
    hi_ok = v < high if high_open else v <= high
    if not (lo_ok and hi_ok):
        lb = "(" if low_open else "["
        rb = ")" if high_open else "]"
        hi = "inf" if high == math.inf else high
        raise ValueError(f"{name} must be in {lb}{low}, {hi}{rb}, got {value!r}")
    return v


def t_star(r: float, tau: float = 0.0) -> float:
    """Normalized real-time ability ``T*(r)``.

    ``T*(r) = 1 / (1 + r^2) * exp(-tau * max(0, r - 1))``

    Args:
        r: Normalized runtime ``t_total / t_max``, ``r >= 0``. ``r = 1`` means
            the agent used exactly its time budget.
        tau: Deadline strictness, ``tau >= 0``. ``tau = 0`` is permissive
            (no extra penalty past the deadline); larger ``tau`` penalizes
            overruns ``r > 1`` more aggressively.

    Returns:
        A value in ``(0, 1]``, equal to ``1`` only at ``r = 0``.

    Raises:
        ValueError: if ``r`` or ``tau`` is negative, ``nan``, or ``inf``.
    """
    r = _check("r", r)
    tau = _check("tau", tau)
    return (1.0 / (1.0 + r ** 2)) * math.exp(-tau * max(0.0, r - 1.0))


def grace(A: float, r: float, beta: float = 1.0, tau: float = 0.0) -> float:
    """Compute the GRACE score.

    ``GRACE(A, r; beta, tau) = (1 + beta^2) * A * T*(r) / (beta^2 * A + T*(r))``

    This is the weighted harmonic mean of accuracy ``A`` and real-time
    ability ``T*(r)``, generalizing the F-beta score: ``beta`` sets the
    accuracy/speed trade-off and ``tau`` sets deadline strictness.

    Args:
        A: Success rate (accuracy) in ``[0, 1]``.
        r: Normalized runtime ``t_total / t_max``, ``r >= 0``.
        beta: Accuracy-vs-speed balance, ``beta >= 0``. Following the F-beta
            convention, ``beta`` multiplies accuracy in the denominator, so
            ``beta = 1`` weights accuracy and speed equally; ``beta > 1``
            emphasizes speed (real-time ability ``T*``); ``beta < 1``
            emphasizes accuracy ``A``.
        tau: Deadline strictness passed to :func:`t_star`.

    Returns:
        GRACE score in ``[0, 1]``. Returns ``0.0`` when both ``A`` and
        ``T*(r)`` are zero (degenerate denominator).

    Raises:
        ValueError: if any argument is out of range, ``nan``, or ``inf``
            (``A`` must be in ``[0, 1]``; ``r``, ``beta``, ``tau >= 0``).
    """
    A = _check("A", A, high=1.0)
    beta = _check("beta", beta)
    Ts = t_star(r, tau)
    numerator = (1.0 + beta ** 2) * A * Ts
    denominator = beta ** 2 * A + Ts
    if denominator == 0:
        return 0.0
    return numerator / denominator


def weights_to_params(w_beta: float, w_tau: float):
    """Map intuitive preference weights to raw ``(beta, tau)`` parameters.

    ``beta = sqrt(w_beta / (1 - w_beta))`` and ``tau = w_tau / (1 - w_tau)``.

    Larger ``w_beta`` -> larger ``beta`` -> more emphasis on speed; see
    :func:`grace`. Lets users specify a balance preference (``w_beta``) and
    "how strict is my deadline" (``w_tau``) on a ``[0, 1)`` scale instead of
    reasoning about the raw parameters.

    Args:
        w_beta: Accuracy/speed balance in ``[0, 1)``. ``0.5`` -> ``beta = 1``
            (equal weight); higher -> more speed emphasis.
        w_tau: Deadline-strictness preference in ``[0, 1)``. ``0`` -> ``tau = 0``.

    Returns:
        Tuple ``(beta, tau)`` for use with :func:`grace`.

    Raises:
        ValueError: if ``w_beta`` or ``w_tau`` is outside ``[0, 1)``, ``nan``,
            or ``inf`` (``1`` is excluded to avoid division by zero).
    """
    w_beta = _check("w_beta", w_beta, high=1.0, high_open=True)
    w_tau = _check("w_tau", w_tau, high=1.0, high_open=True)
    beta = math.sqrt(w_beta / (1.0 - w_beta))
    tau = w_tau / (1.0 - w_tau)
    return beta, tau
