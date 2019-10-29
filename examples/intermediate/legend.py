"""
======
Legend
======

The legend can be put using ``ax.legend`` in the same way as Matplotlib.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_scatter_points


ax = plt.subplot(projection='ternary')

for seed in [1, 9, 6, 8]:
    ax.scatter(*get_scatter_points(11, seed=seed), alpha=0.5, label=seed)

ax.legend()

plt.show()
