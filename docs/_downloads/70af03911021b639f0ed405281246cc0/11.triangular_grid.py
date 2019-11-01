"""
===============
Triangular grid
===============

A triangular grid can be plotted by giving the grid points to ``ax.triplot``.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_triangular_grid


t, l, r = get_triangular_grid()

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(wspace=0.3)

ax = fig.add_subplot(121, projection='ternary')
ax.triplot(t, l, r)

ax = fig.add_subplot(122, projection='ternary')
ax.triplot(t, l, r, marker='o')

plt.show()
