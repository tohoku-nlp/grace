"""GRACE: a tunable metric unifying accuracy and efficiency for robotics evaluation.

Quickstart::

    from grace_metric import grace

    # 80% success, used 1.5x the time budget, equal weight, permissive deadline
    score = grace(A=0.80, r=1.5, beta=1.0, tau=0.0)

See https://github.com/tohoku-nlp/grace for benchmarks and the paper.
"""

from .core import t_star, grace, weights_to_params
from .baselines import sr_only, sr_over_time, weighted_sum, spl
from .regimes import REGIMES, compute_all_metrics

__version__ = "0.1.0"

__all__ = [
    "grace",
    "t_star",
    "weights_to_params",
    "sr_only",
    "sr_over_time",
    "weighted_sum",
    "spl",
    "REGIMES",
    "compute_all_metrics",
    "__version__",
]
