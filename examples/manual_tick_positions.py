"""
=====================
Manual tick positions
=====================

Tick positions can be given manually in the same way as Matplotlib.

This feature may be useful e.g. when you do not want to show zero ticks to make
corner axis labels closer to the triangle.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


ax = plt.subplot(projection='ternary')

ax.plot(*get_spiral())

ax.grid()

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

# Specify tick positions manually.
ax.taxis.set_ticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.laxis.set_ticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.raxis.set_ticks([0.2, 0.4, 0.6, 0.8, 1.0])

plt.show()
