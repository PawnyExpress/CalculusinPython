"""calc — reusable helpers extracted from the calculus notebooks.

Import what you need in any notebook (the Jupyter kernel runs from the repo
root, so this just works):

    from calc import numerical_slope, numerical_limit, symbolic_limit, plot_function

Submodules:
    calc.numerical — difference quotients & one-sided limit estimates
    calc.symbolic  — exact limits / solving with SymPy
    calc.plotting  — matplotlib graphing helper
"""
from .numerical import (
    central_slope,
    end_behavior,
    limit_at_infinity,
    numerical_limit,
    numerical_limit_close,
    numerical_slope,
    one_sided_values,
    slope_table,
    slope_table_central,
)
from .plotting import plot_function
from .symbolic import (
    solve_equation,
    symbolic_limit,
    symbolic_limit_safe,
    undefined_points,
)

__all__ = [
    # --- original (notebook) versions, kept for teaching ---
    "numerical_slope",
    "slope_table",
    "one_sided_values",
    "numerical_limit",
    "limit_at_infinity",
    "symbolic_limit",
    # --- refined versions (prefer these) ---
    "central_slope",
    "slope_table_central",
    "numerical_limit_close",
    "end_behavior",
    "symbolic_limit_safe",
    # --- unchanged helpers ---
    "solve_equation",
    "undefined_points",
    "plot_function",
]
