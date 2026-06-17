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
    limit_at_infinity,
    numerical_limit,
    numerical_slope,
    one_sided_values,
    slope_table,
)
from .plotting import plot_function
from .symbolic import solve_equation, symbolic_limit, undefined_points

__all__ = [
    "numerical_slope",
    "slope_table",
    "one_sided_values",
    "numerical_limit",
    "limit_at_infinity",
    "solve_equation",
    "undefined_points",
    "symbolic_limit",
    "plot_function",
]
