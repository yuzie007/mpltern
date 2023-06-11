"""
=====================
Cartesian coordinates
=====================

In mpltern, the x- and y-limits are initially
[−3\ :sup:`−1/2`, +3\ :sup:`−1/2`] and [0, 1], respectively.
The triangle vertices are, by default,
(0, 1), (−3\ :sup:`−1/2`, 0), (+3\ :sup:`−1/2`, 0).

In most methods, we can still plot in Cartesian coordinates rather than in
ternary coordinates by using `Matplotlib transforms
<https://matplotlib.org/stable/tutorials/advanced/transforms_tutorial.html>`__
like `ax.transData`, `ax.transAxes`, `fig.transFigure`.
"""
import numpy as np
import matplotlib.pyplot as plt
import mpltern


def plot_frame(ax):
    """Plot frame of the original Axes."""
    ax.fill(
        [0, 0, 1, 1],
        [0, 1, 1, 0],
        ec="k",
        fc="none",
        ls=":",
        clip_on=False,
        transform=ax.transAxes,
    )


ax = plt.subplot(projection='ternary')
plot_frame(ax)


# %%
# This may be useful to plot e.g. the subfigure label as well as to understand
# the legend position.
fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(wspace=0.3)

ax = fig.add_subplot(1, 2, 1, projection='ternary')
plot_frame(ax)
x = [-1.0 / np.sqrt(3.0), +0.5 / np.sqrt(3.0)]
y = [0.0, 0.5]
ax.plot(x, y, label="a", transform=ax.transData)
ax.legend(loc=1)
ax.text(0.02, 0.94, "(a)", ha="left", transform=ax.transAxes)

ax = fig.add_subplot(1, 2, 2, projection='ternary')
plot_frame(ax)
x = [+1.0 / np.sqrt(3.0), -0.5 / np.sqrt(3.0)]
y = [0.0, 0.5]
ax.plot(x, y, label="b", transform=ax.transData)
ax.legend(loc=2)
ax.text(0.98, 0.94, "(b)", ha="right", transform=ax.transAxes)

plt.show()

# %%
