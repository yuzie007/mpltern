"""
=======================
Plotting region fitting
=======================

When the ternary limits are modified, the plotting region can be expanded or
cropped in a different way via the `fit` option in e.g. `set_ternary_lim`.

- `'rectangle'` (default): Fitted to the original rectangle.
- `'triangle'`: Fitted to the original triangle.
- `'none'`: The plotting region is simply cropped (or expanded).
"""
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral


def set_labels(ax):
    """Set ternary-axis labels."""
    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')
    ax.taxis.set_label_position("tick1")
    ax.laxis.set_label_position("tick1")
    ax.raxis.set_label_position("tick1")


def plot_frame(ax):
    ax.fill(
        [0.0, 0.0, 1.0, 1.0],
        [0.0, 1.0, 1.0, 0.0],
        ec="r",
        fc="none",
        ls=":",
        transform=ax.transAxes,
        clip_on=False,
        zorder=1.0,
    )
    ax.fill(
        [0.5, 0.0, 1.0],
        [1.0, 0.0, 0.0],
        ec="b",
        fc="none",
        ls=":",
        transform=ax.transAxes,
        clip_on=False,
        zorder=1.0,
    )


fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(left=0.075, right=0.925, wspace=0.25)

fits = ["rectangle", "triangle", "none"]
for i, fit in enumerate(fits):
    ax = fig.add_subplot(1, 3, i + 1, projection='ternary')
    ax.plot(*get_spiral(), c="k")
    ax.set_ternary_lim(
        0.1, 0.7,  # tmin, tmax
        0.1, 0.7,  # lmin, lmax
        0.1, 0.7,  # rmin, rmax
        fit=fit,
    )
    set_labels(ax)
    ax.set_title(f"fit='{fit}'", pad=42)

    plot_frame(ax)

plt.show()
