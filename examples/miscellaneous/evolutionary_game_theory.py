"""
========================
Evolutionary game theory
========================

`replicator equation <https://en.wikipedia.org/wiki/Replicator_equation>`__

.. warning::
    The implementation of mathematics might be wrong due to my lack of
    knowledge.
"""
import matplotlib.pyplot as plt
import numpy as np
from mpltern.datasets import get_triangular_grid

x = np.array(get_triangular_grid(25))

payoff_matrix = [
    [0.0, -1.0, 1.0],
    [1.0, 0.0, -1.0],
    [-1.0, 1.0, 0.0],
]

fitness = payoff_matrix @ x
d = (fitness - np.sum(fitness * x, axis=0)) * x
norm = np.linalg.norm(d, axis=0)

ax = plt.subplot(projection="ternary")

ax.tripcolor(*x, norm, cmap="turbo", shading="gouraud", rasterized=True)

ax.quiver(*x, *d, scale=5, clip_on=False)

ax.set_tlabel("$x_0$")
ax.set_llabel("$x_1$")
ax.set_rlabel("$x_2$")

plt.show()
