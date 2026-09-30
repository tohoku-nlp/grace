# GRACE

**G**eneralized **R**obotics **A**ccuracy-**C**ompletion **E**valuation — a tunable
metric that unifies task success rate and time efficiency for robotics evaluation.

Robotics papers usually report success rate and timing separately, which hides
accuracy/efficiency trade-offs and makes cross-benchmark comparison hard. GRACE
combines the two into a single, interpretable score via a tunable harmonic mean
inspired by the F-beta score:

```
GRACE(A, r; β, τ) = (1 + β²) · A · T*(r) / (β² · A + T*(r))
T*(r)             = 1 / (1 + r²) · exp(−τ · max(0, r − 1))
```

where `A` is the success rate in `[0, 1]` and `r = t_total / t_max` is the
runtime normalized by a time budget. Two parameters make domain priorities
explicit: **β** balances accuracy against speed and **τ** sets deadline
strictness. Success-rate-only and pure-efficiency scores arise as limiting cases.

This repository accompanies the paper *"GRACE: A Tunable Metric Unifying
Accuracy and Efficiency for Robotics Evaluation"* (IROS 2026).

## Installation

```bash
pip install grace_metric
```

Or from source:

```bash
git clone https://github.com/tohoku-nlp/grace
cd grace
pip install -e .
```

The core metric is **pure Python with no dependencies**. The benchmark
reproduction scripts additionally need `matplotlib` and `numpy`:

```bash
pip install "grace_metric[benchmarks]"
```

## Quickstart

```python
from grace_metric import grace

# 80% success, used 1.5x the time budget, equal accuracy/speed weight,
# permissive deadline:
grace(A=0.80, r=1.5, beta=1.0, tau=0.0)   # -> 0.444
```

### Choosing β and τ

| Parameter | Meaning | Effect |
|-----------|---------|--------|
| `beta`    | Accuracy ↔ speed balance | `beta = 1` weights equally; `beta > 1` emphasizes speed; `beta < 1` emphasizes accuracy |
| `tau`     | Deadline strictness      | `tau = 0` is permissive; larger `tau` penalizes overruns (`r > 1`) more sharply |

If you prefer to think on a `[0, 1)` scale, map intuitive preference weights to
the internal parameters:

```python
from grace_metric import weights_to_params, grace

beta, tau = weights_to_params(w_beta=0.5, w_tau=0.3)
grace(0.8, 1.5, beta=beta, tau=tau)
```

### Interactive parameter explorer

To choose `beta` and `tau` visually, open the notebook in `notebooks/`:

```bash
pip install "grace_metric[notebook]"
jupyter lab notebooks/parameter_explorer.ipynb
```

Drag the sliders and watch the score landscape, the time-penalty curve
`T*(r)`, and the trade-off (indifference) contours redraw live, then copy the
parameters you settle on. The notebook is **self-contained** -- it falls back to
a built-in copy of the formulas when the package is not installed, so it also
runs on **Google Colab** with no setup (upload it and *Runtime -> Run all*).
See `notebooks/README.md` for details.

### Preset regimes

Three calibrated presets used in the paper's benchmark rescoring:

```python
from grace_metric import grace, REGIMES

grace(0.8, 1.5, **REGIMES["moderate"])     # beta=1.0, tau=0.43
# REGIMES.keys() -> "permissive", "moderate", "strict"
# each maps to a dict, e.g. REGIMES["strict"] == {"beta": 2.0, "tau": 5.67}
```

### Baselines and all-in-one helper

```python
from grace_metric import compute_all_metrics

compute_all_metrics(A=0.8, r=1.5)
# {'SR': ..., 'SR/Time': ..., 'WSum_0.5': ..., 'SPL': ...,
#  'GRACE_permissive': ..., 'GRACE_moderate': ..., 'GRACE_strict': ...}
```

The baseline metrics (`sr_only`, `sr_over_time`, `weighted_sum`, `spl`) are also
importable individually.

## Citation

If you use GRACE, please cite:

```bibtex
@inproceedings{sakaguchi2026grace,
  title     = {{GRACE}: A Tunable Metric Unifying Accuracy and Efficiency for Robotics Evaluation},
  author    = {Sakaguchi, Keisuke},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  year      = {2026},
}
```

## License

Apache License 2.0 — see [LICENSE](LICENSE) and [NOTICE](NOTICE).
