"""
==================
Manual tick labels
==================

Tick labels can be given manually in the same way as Matplotlib.
"""
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral


ax = plt.subplot(projection='ternary')

ax.plot(*get_spiral())

# Specify tick positions manually.
ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
labels = ["0/5", "1/5", "2/5", "3/5", "4/5", "5/5"]
ax.taxis.set_ticks(ticks, labels=labels)
ax.laxis.set_ticks(ticks, labels=labels)
ax.raxis.set_ticks(ticks, labels=labels)

plt.show()
