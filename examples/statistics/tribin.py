"""
======
TriBin
======

`ax.tribin` is a 2D histogram plot, in which the bins are triangles and
the color represents the number of data points within each bin.
Unlike Matplotlib, `gridsize` (by default 100) can be only a single int.

.. note::

    Available with ``mpltern>=0.5.0``
"""
import numpy as np

import matplotlib.pyplot as plt
import mpltern

np.random.seed(19680801)
t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=100000).T

# %%
ax = plt.subplot(projection="ternary")

# If "edgecolors=face" (default), small triangles look overlapping.
ax.tribin(t, l, r, edgecolors="none")

plt.show()

# %%
ax = plt.subplot(projection="ternary")

ax.tribin(t, l, r, bins="log", edgecolors="none")

plt.show()
