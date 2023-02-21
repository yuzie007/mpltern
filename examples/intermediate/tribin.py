"""
======
TriBin
======

``ax.tribin`` is a 2D histogram plot, in which the bins are triangles and
the color represents the number of data points within each bin.

Unlike Matplotlib, `gridsize` can be only a single int.
"""
import numpy as np

import matplotlib.pyplot as plt
import mpltern

np.random.seed(19680801)
t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=100000).T
ax = plt.subplot(projection="ternary")
# If "face" (default), small triangles look overlapping with each other.
ax.tribin(t, l, r, edgecolors="none")

plt.show()
