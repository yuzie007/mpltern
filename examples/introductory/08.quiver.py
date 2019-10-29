"""
======
Quiver
======

2D field of arrows can be plotted using ``ax.quiver``.
"""
import numpy as np

import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_triangular_grid


t, l, r = get_triangular_grid()

# Arrows. The sum of the three must be zero.
dt = 1.0 / 3.0 - t
dl = 1.0 / 3.0 - l
dr = 1.0 / 3.0 - r

length = np.sqrt(dt ** 2 + dl ** 2 + dr ** 2)

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(left=0.075, right=0.85, wspace=0.3)

ax = fig.add_subplot(121, projection='ternary')
pc = ax.quiver(t, l, r, dt, dl, dr)

ax = fig.add_subplot(122, projection='ternary')
pc = ax.quiver(t, l, r, dt, dl, dr, length)

cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
colorbar = fig.colorbar(pc, cax=cax)
colorbar.set_label('Length', rotation=270, va='baseline')

plt.show()
