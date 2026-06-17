"""Numerical (approximation-based) calculus helpers.

These package up the hand-computed difference-quotient and one-sided-limit
techniques from the notebooks into reusable functions. Pass in any Python
function ``f`` (e.g. ``lambda x: x**2``).
"""
from __future__ import annotations

import math
from typing import Callable, Iterable, Optional


def numerical_slope(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Approximate the slope (derivative) of ``f`` at ``x``.

    Uses the **forward** difference quotient ``(f(x + h) - f(x)) / h``. Smaller
    ``h`` gives a closer approximation (down to floating-point limits).

    .. note::
       This is the version straight from the notebooks. It is kept as-is so the
       shortcomings below are visible side-by-side with the refined
       :func:`central_slope`. **Prefer** :func:`central_slope` for real work.

       Why this version is weaker:

       1. **Accuracy.** The forward difference has truncation error that shrinks
          only *linearly* with ``h`` (it is O(h)). Halving ``h`` only roughly
          halves the error, so you need a very small ``h`` to get a good answer.
       2. **It is biased.** It measures the slope of the line from ``x`` to
          ``x + h`` — a point that sits entirely on *one side* of ``x``. So the
          estimate is really the slope a little to the *right* of ``x``, not at
          ``x`` itself. For a curve like ``x**2`` at ``x=1`` it overshoots the
          true slope of 2 unless ``h`` is tiny.
       3. **Floating-point floor.** Because you must drive ``h`` very small to
          fight (1), you run into subtractive cancellation: ``f(x + h)`` and
          ``f(x)`` become nearly equal, the leading digits cancel, and the
          result *degrades* once ``h`` drops below ~1e-8. See
          :func:`slope_table`.

    >>> round(numerical_slope(lambda x: x**2, 1), 4)
    2.0
    """
    return (f(x + h) - f(x)) / h


def central_slope(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """Approximate the slope of ``f`` at ``x`` with the **central** difference.

    Uses ``(f(x + h) - f(x - h)) / (2 * h)`` — it straddles ``x`` symmetrically,
    sampling equally on both sides. This is the refinement of
    :func:`numerical_slope`; reach for it by default.

    Why it is better:

    1. **Accuracy.** The symmetric form cancels the first-order error term, so
       its truncation error shrinks *quadratically* with ``h`` (it is O(h**2)).
       Halving ``h`` cuts the error by ~4×, not 2×. At ``h = 1e-5`` it is
       already accurate to roughly 10 decimal places, where the forward
       difference is good to only ~5.
    2. **No directional bias.** Because it averages the left and right behavior
       around ``x``, the estimate is centered *on* ``x`` rather than drifting to
       the right. For ``x**2`` at ``x=1`` it returns 2.0 almost exactly even
       with a fairly large ``h``.
    3. **It tolerates a larger ``h``.** Since you don't need a microscopic ``h``
       to get accuracy, you stay well clear of the subtractive-cancellation
       floor that wrecks the forward difference at very small ``h``.

    >>> round(central_slope(lambda x: x**2, 1), 10)
    2.0
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def slope_table(
    f: Callable[[float], float],
    x: float,
    powers: Iterable[int] = range(1, 11),
) -> list[tuple[float, float]]:
    """Show the slope converging as ``h`` shrinks (forward difference).

    Returns a list of ``(h, slope)`` pairs for ``h = 10**-a`` over ``powers`` —
    the same loop the notebooks use to watch the estimate settle on the answer.

    Run this and watch closely: the estimate improves as ``h`` shrinks, then
    around ``a = 8`` it *stops improving and starts getting worse*. That is the
    subtractive-cancellation floor described in :func:`numerical_slope`, and it
    quietly contradicts the notebook's comment that "smaller h is always
    better." Compare with :func:`slope_table_central` to see the difference.
    """
    return [(10 ** (-a), numerical_slope(f, x, 10 ** (-a))) for a in powers]


def slope_table_central(
    f: Callable[[float], float],
    x: float,
    powers: Iterable[int] = range(1, 11),
) -> list[tuple[float, float]]:
    """Same convergence loop as :func:`slope_table`, but central difference.

    Returns ``(h, slope)`` pairs computed with :func:`central_slope`. Lined up
    against :func:`slope_table`, this makes the refinement concrete: the central
    estimates lock onto the true slope far sooner (by ``a = 5`` or so) and hold
    steady, instead of overshooting and then decaying once ``h`` gets tiny.
    """
    return [(10 ** (-a), central_slope(f, x, 10 ** (-a))) for a in powers]


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

    .. note::
       Kept as-is from the notebook to show *why* the rounding test is unsafe;
       use :func:`numerical_limit_close` instead. The ``round(left) !=
       round(right)`` comparison has two conceptual flaws:

       1. **False "exists" for close-but-different limits.** ``round`` snaps to
          the nearest integer, so a left limit of 2.4 and a right limit of 2.6
          both round to 2 — the function reports the limit *exists* and equal
          when the one-sided limits genuinely disagree.
       2. **False "does not exist" near a half-integer.** Two sides that are
          truly converging to the same value, say 2.499 and 2.501, round to 2
          and 3 and get flagged as a non-existent limit. The verdict hinges on
          which side of ``x.5`` the values land, which has nothing to do with
          the math.

       The fix is to compare the two sides against a real *tolerance* rather
       than rounding to integers (see :func:`numerical_limit_close`).
    """
    left, right = one_sided_values(f, x, h)
    if round(left) != round(right):
        return None, left, right
    return (left + right) / 2, left, right


def numerical_limit_close(
    f: Callable[[float], float],
    x: float,
    h: float = 1e-5,
    rel_tol: float = 1e-3,
    abs_tol: float = 1e-6,
) -> tuple[Optional[float], float, float]:
    """Refined two-sided limit estimate using a real tolerance, not rounding.

    Returns ``(estimate, left, right)``. The left and right one-sided values are
    compared with :func:`math.isclose`, so "do the two sides agree?" becomes a
    question of *how far apart they are* rather than *which integer they round
    to*. This fixes both failure modes of :func:`numerical_limit`:

    * limits like 2.4 vs 2.6 are now correctly reported as **non-existent**
      (their gap exceeds the tolerance), and
    * sides converging to a half-integer like 2.499 vs 2.501 are correctly
      reported as **existing** (their gap is within the tolerance).

    ``rel_tol`` scales with the magnitude of the values (good for large limits);
    ``abs_tol`` provides a floor so values near zero still compare sensibly.

    >>> est, *_ = numerical_limit_close(lambda v: v + 2.5, 0)
    >>> round(est, 3)
    2.5
    """
    left, right = one_sided_values(f, x, h)
    if not math.isclose(left, right, rel_tol=rel_tol, abs_tol=abs_tol):
        return None, left, right
    return (left + right) / 2, left, right


def limit_at_infinity(
    f: Callable[[float], float],
    values: Iterable[float] = (10, 100, 1000, 10000),
) -> list[tuple[float, float]]:
    """Evaluate ``f`` at increasingly large ``x`` to observe end behavior.

    Returns ``(x, f(x))`` pairs so you can see what value the function trends
    toward as ``x`` grows.

    .. note::
       Kept from the notebook. The conceptual gap: it only walks ``x`` toward
       **+∞**. "End behavior" is a two-ended idea — a function can approach
       different values (or none) as ``x → -∞`` versus ``x →
       +∞`` (e.g. ``arctan`` heads to ``-π/2`` on the left and
       ``+π/2`` on the right). Looking at only the positive side tells you
       half the story. Use :func:`end_behavior` to see both ends.
    """
    return [(v, f(v)) for v in values]


def end_behavior(
    f: Callable[[float], float],
    magnitudes: Iterable[float] = (10, 100, 1000, 10000),
) -> tuple[list[tuple[float, float]], list[tuple[float, float]]]:
    """Observe end behavior at **both** ``-∞`` and ``+∞``.

    Returns ``(toward_neg_inf, toward_pos_inf)``, each a list of ``(x, f(x))``
    pairs. ``toward_pos_inf`` walks ``x`` out through the given ``magnitudes``;
    ``toward_neg_inf`` walks the negatives of the same magnitudes (ordered most-
    negative first, so each list reads in the direction of travel toward its
    infinity). This is the refinement of :func:`limit_at_infinity`: it shows the
    full two-ended picture instead of only the positive tail.

    >>> neg, pos = end_behavior(lambda v: 1 / v, magnitudes=(10, 100))
    >>> pos[-1][1] > 0 and neg[-1][1] < 0
    True
    """
    mags = list(magnitudes)
    toward_pos_inf = [(m, f(m)) for m in mags]
    toward_neg_inf = [(-m, f(-m)) for m in reversed(mags)]
    return toward_neg_inf, toward_pos_inf
