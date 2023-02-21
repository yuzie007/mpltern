"""
================
Binned & scatter
================

A binned plot can be shown together with a scatter plot.
"""
import numpy as np

import matplotlib.pyplot as plt
import mpltern

np.random.seed(19680801)
t, l, r = np.random.dirichlet(alpha=(2.0, 2.0, 2.0), size=100).T

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(left=0.075, right=0.85, wspace=0.3)

ax = fig.add_subplot(1, 2, 1, projection="ternary")
ax.scatter(t, l, r, color="C3", marker="x")
pc = ax.hexbin(t, l, r, gridsize=10, edgecolors="k", alpha=0.5, zorder=0.0)
ax.set_title("hexbin")

cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
colorbar = fig.colorbar(pc, cax=cax)
colorbar.set_label("Count", rotation=270, va="baseline")

ax = fig.add_subplot(1, 2, 2, projection="ternary")
ax.scatter(t, l, r, color="C3", marker="x")
pc = ax.tribin(t, l, r, gridsize=10, edgecolors="k", alpha=0.5, zorder=0.0)
ax.set_title("tribin")

cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
colorbar = fig.colorbar(pc, cax=cax)
colorbar.set_label("Count", rotation=270, va="baseline")

plt.show()
