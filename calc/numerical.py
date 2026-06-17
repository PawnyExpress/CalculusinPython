"""Numerical (approximation-based) calculus helpers.

These package up the hand-computed difference-quotient and one-sided-limit
techniques from the notebooks into reusable functions. Pass in any Python
function ``f`` (e.g. ``lambda x: x**2``).
"""
from __future__ import annotations

from typing import Callable, Iterable, Optional


def numerical_slope(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Approximate the slope (derivative) of ``f`` at ``x``.

    Uses the difference quotient ``(f(x + h) - f(x)) / h``. Smaller ``h`` gives
    a closer approximation (down to floating-point limits).

    >>> round(numerical_slope(lambda x: x**2, 1), 4)
    2.0
    """
    return (f(x + h) - f(x)) / h


def slope_table(
    f: Callable[[float], float],
    x: float,
    powers: Iterable[int] = range(1, 11),
) -> list[tuple[float, float]]:
    """Show the slope converging as ``h`` shrinks.

    Returns a list of ``(h, slope)`` pairs for ``h = 10**-a`` over ``powers`` —
    the same loop the notebooks use to watch the estimate settle on the answer.
    """
    return [(10 ** (-a), numerical_slope(f, x, 10 ** (-a))) for a in powers]


def one_sided_values(
    f: Callable[[float], float], x: float, h: float = 1e-5
) -> tuple[float, float]:
    """Return ``(left, right)`` estimates of ``f`` just below and above ``x``."""
    return f(x - h), f(x + h)


def numerical_limit(
    f: Callable[[float], float], x: float, h: float = 1e-5
) -> tuple[Optional[float], float, float]:
    """Estimate the two-sided limit of ``f`` at ``x`` from one-sided values.

    Returns ``(estimate, left, right)``. If the rounded left/right values
    disagree the limit is treated as nonexistent and ``estimate`` is ``None``
    (mirroring the notebook's ``round(y_right) != round(y_left)`` check).
    """
    left, right = one_sided_values(f, x, h)
    if round(left) != round(right):
        return None, left, right
    return (left + right) / 2, left, right


def limit_at_infinity(
    f: Callable[[float], float],
    values: Iterable[float] = (10, 100, 1000, 10000),
) -> list[tuple[float, float]]:
    """Evaluate ``f`` at increasingly large ``x`` to observe end behavior.

    Returns ``(x, f(x))`` pairs so you can see what value the function trends
    toward as ``x`` grows.
    """
    return [(v, f(v)) for v in values]
