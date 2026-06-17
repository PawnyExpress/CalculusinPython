"""Symbolic calculus helpers built on SymPy (exact, not approximate).

Where :mod:`calc.numerical` estimates with small numbers, these return exact
answers like ``oo`` (infinity) or ``3`` using SymPy's algebra engine.
"""
from __future__ import annotations

import sympy
from sympy import Symbol, oo, solve, symbols  # noqa: F401  (re-exported for convenience)

x = symbols("x")  # a ready-to-use symbol so notebooks can just `from calc.symbolic import x`


def solve_equation(expr, var: Symbol = x):
    """Solve ``expr = 0`` for ``var`` and return the list of solutions.

    >>> solve_equation(x**2 - 4)
    [-2, 2]
    """
    return solve(sympy.sympify(expr), var)


def undefined_points(expr, var: Symbol = x):
    """Find where a rational expression is undefined (its denominator is zero).

    >>> undefined_points(3 * x**2 / (x**2 - 4))
    [-2, 2]
    """
    _, denominator = sympy.together(sympy.sympify(expr)).as_numer_denom()
    return solve(denominator, var)


def symbolic_limit(expr, point, var: Symbol = x, direction: str = "both"):
    """Compute an exact limit of ``expr`` as ``var`` approaches ``point``.

    ``direction`` is ``'+'`` (from the right), ``'-'`` (from the left), or
    ``'both'`` (returns a ``(right, left)`` tuple). Use ``sympy.oo`` for the
    point to take a limit at infinity.

    >>> symbolic_limit(3 * x**2 / (x**2 - 4), oo, direction='+')
    3
    """
    expr = sympy.sympify(expr)
    if direction == "+":
        return sympy.limit(expr, var, point, "+")
    if direction == "-":
        return sympy.limit(expr, var, point, "-")
    return sympy.limit(expr, var, point, "+"), sympy.limit(expr, var, point, "-")
