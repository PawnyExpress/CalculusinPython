"""Plotting helpers for visualising functions and key points.

Wraps the repeated matplotlib setup from the notebooks (window sizing, x/y
axes through the origin, marked points) into one call.
"""
from __future__ import annotations

from typing import Callable, Iterable, Optional

import matplotlib.pyplot as plt
import numpy as np


def plot_function(
    f: Callable[[np.ndarray], np.ndarray],
    center: float = 0.0,
    zoom: float = 10.0,
    num: int = 400,
    points: Optional[Iterable[tuple[float, float]]] = None,
    title: Optional[str] = None,
    ax: Optional[plt.Axes] = None,
):
    """Plot ``f`` in a square window of half-width ``zoom`` around ``center``.

    Draws the curve, the x and y axes through the origin, and optional marked
    ``points`` (a list of ``(x, y)`` tuples shown as red dots). Returns the
    matplotlib ``Axes`` so you can keep customising it.

    ``f`` should accept a NumPy array (e.g. ``lambda x: x**2``).
    """
    if ax is None:
        _, ax = plt.subplots()

    xmin, xmax = center - zoom, center + zoom
    ymin, ymax = -zoom, zoom

    xs = np.linspace(xmin, xmax, num)
    ax.plot(xs, f(xs))

    for px, py in points or []:
        ax.plot([px], [py], "ro")

    ax.axis([xmin, xmax, ymin, ymax])
    ax.axhline(y=0, color="k")
    ax.axvline(x=0, color="k")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    if title:
        ax.set_title(title)
    return ax
