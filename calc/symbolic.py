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

    .. note::
       Kept as the original to document a genuine bug; prefer
       :func:`symbolic_limit_safe`. When ``direction='both'`` (the **default**)
       and ``point`` is ``±oo``, this computes a "left-hand limit at infinity"
       via ``dir='-'``. That is mathematically meaningless: at infinity there is
       only one side to approach from, so the second element of the returned
       tuple is nonsense. The README sidesteps this by always passing
       ``direction='+'`` for its infinity example — but the *default* path
       silently produces a bogus value, which is exactly the kind of trap a
       teaching tool should not hide.

    >>> symbolic_limit(3 * x**2 / (x**2 - 4), oo, direction='+')
    3
    """
    expr = sympy.sympify(expr)
    if direction == "+":
        return sympy.limit(expr, var, point, "+")
    if direction == "-":
        return sympy.limit(expr, var, point, "-")
    return sympy.limit(expr, var, point, "+"), sympy.limit(expr, var, point, "-")


def symbolic_limit_safe(expr, point, var: Symbol = x, direction: str = "both"):
    """Refined exact limit that handles ``±oo`` correctly.

    Same interface as :func:`symbolic_limit`, with one fix: a two-sided limit is
    only meaningful at a *finite* point. When ``point`` is ``±oo``, "both sides"
    collapses to the single one-sided limit (you can only approach infinity from
    one direction), so a single value is returned instead of a tuple containing
    a meaningless second entry.

    Behavior by case:

    * finite ``point`` + ``direction='both'`` → ``(right, left)`` tuple, as
      before;
    * ``point = +oo`` → the limit approaching from the left (``dir='-'``, i.e.
      coming *up* from finite values), returned as a single value;
    * ``point = -oo`` → the limit approaching from the right (``dir='+'``, i.e.
      coming *down* from finite values), returned as a single value;
    * explicit ``direction='+'`` / ``'-'`` → honored unchanged.

    >>> symbolic_limit_safe(3 * x**2 / (x**2 - 4), oo)
    3
    >>> symbolic_limit_safe(x**2 / (x**2 - 4), 2)   # finite point, two-sided
    (oo, -oo)
    """
    expr = sympy.sympify(expr)
    if direction == "+":
        return sympy.limit(expr, var, point, "+")
    if direction == "-":
        return sympy.limit(expr, var, point, "-")
    # direction == 'both': a two-sided limit only makes sense at a finite point.
    if point in (oo, -oo):
        # Only one side exists at infinity; pick the side that comes from the
        # finite reals and return a single value rather than a bogus tuple.
        side = "-" if point == oo else "+"
        return sympy.limit(expr, var, point, side)
    return sympy.limit(expr, var, point, "+"), sympy.limit(expr, var, point, "-")
