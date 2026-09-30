# GRACE Parameter Explorer

`parameter_explorer.ipynb` is an interactive notebook for choosing the GRACE
parameters `(beta, tau)` that match your application's accuracy/speed
preferences. Drag the sliders and the score landscape, the time-penalty curve
`T*(r)`, and the trade-off (indifference) contours redraw live; copy the
parameters you settle on from the final **Export** cell.

**The notebook is self-contained.** It uses the `grace_metric` package if it is
installed, but otherwise falls back to a built-in copy of the published formulas
(verified bit-identical to the package), so it needs no install or checkout to
run -- ideal for Google Colab.

## Start it

### Option A — Google Colab (no setup)

1. Go to <https://colab.research.google.com> -> **File -> Upload notebook** and
   choose `parameter_explorer.ipynb` (or open it from GitHub via
   *File -> Open notebook -> GitHub*).
2. **Runtime -> Run all.** Colab already ships `numpy`, `matplotlib`, and
   `ipywidgets`, so the sliders just work.

### Requirements (local runs only)

`numpy`, `matplotlib`, `ipywidgets`, and a Jupyter front-end. The easiest way is
the package's `notebook` extra (installs all of them, including JupyterLab):

```bash
pip install "grace_metric[notebook]"
```

Or install the pieces directly:

```bash
pip install numpy matplotlib ipywidgets jupyterlab
```

### Option B — JupyterLab in the browser

From the repository root (`grace/`):

```bash
jupyter lab notebooks/parameter_explorer.ipynb
```

This serves on `http://localhost:8888` and opens your browser. If you are in a
container or on a remote host, forward port 8888 first (e.g. VS Code "Ports"
panel, or `ssh -L 8888:localhost:8888 <host>`), then open the printed URL.

### Option C — VS Code / Cursor

1. Open `notebooks/parameter_explorer.ipynb` in the editor.
2. Top-right **Select Kernel** -> choose a Python interpreter that has
   `numpy`, `matplotlib`, and `ipywidgets`.
3. **Run All**. The widgets render inline.

## Using the notebook

1. **Run all cells once** (`Run -> Run All Cells`). Each interactive section
   builds its widget when its cell runs, so a fresh kernel needs every cell
   executed before the sliders appear.
2. Drag the sliders in each section:
   - **1. Score landscape** -- GRACE contour over accuracy `A` and runtime `r`,
     with `beta`/`tau` sliders and a movable operating point.
   - **2. Time-penalty curve `T*(r)`** -- pick `tau` from a deadline policy.
   - **3. Trade-off (indifference) curves** -- "if accuracy drops by dA, how much
     faster must the method be to keep the same score?"
   - **4. Export** -- prints a ready-to-paste `grace(A, r, beta=..., tau=...)`
     snippet and the closest named regime.

## Stopping the server

Press `Ctrl-C` in the terminal running JupyterLab, or from another terminal:

```bash
jupyter lab stop 8888
```
