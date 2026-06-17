# Calculus in Python

Calculus curriculum coded in Python — migrated from Google Colab to a local VSCode workflow.

## Contents

- `notebooks/` — Jupyter notebooks (the calc concepts, same `.ipynb` files used in Colab)
  - `LimitsandSlope.ipynb`
  - `CalculusWithPythonLimits_py.ipynb`
- `src/` — reusable Python modules (helpers extracted from notebooks)

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
