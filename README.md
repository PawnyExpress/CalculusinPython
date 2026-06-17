# Calculus in Python

Calculus curriculum coded in Python — migrated from Google Colab to a local VSCode workflow.

## Contents

- `notebooks/` — Jupyter notebooks (the calc concepts, same `.ipynb` files used in Colab)
  - `LimitsandSlope.ipynb`
  - `CalculusWithPythonLimits_py.ipynb`
- `calc/` — reusable Python package (helpers extracted from the notebooks)
  - `numerical.py` — difference quotients & one-sided limit estimates
  - `symbolic.py` — exact limits / equation solving with SymPy
  - `plotting.py` — matplotlib graphing helper

## Using the `calc` helpers in a notebook

The Jupyter kernel runs from the repo root, so importing just works — no path setup:

```python
from calc import numerical_slope, numerical_limit, symbolic_limit, plot_function
from calc.symbolic import x          # a ready-made SymPy symbol

numerical_slope(lambda v: v**2, 1)   # ≈ 2.0   (slope of y=x² at x=1)
symbolic_limit(3*x**2/(x**2-4), 2, direction='+')   # exact: oo
plot_function(lambda v: v**2, center=1, points=[(1, 1)], title="y=x²")
```

## Setup

```powershell
# 1. Create a virtual environment
python -m venv .venv

# 2. Activate it (PowerShell)
.\.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt
```

## Working in VSCode

1. Install the **Python** and **Jupyter** extensions.
2. Open a notebook in `notebooks/`.
3. Select the `.venv` interpreter as the kernel (top-right of the notebook).
4. Run cells with `Shift+Enter` — same as Colab.

## Dependencies

- numpy
- matplotlib
- sympy
- jupyter / ipykernel
