"""
======
Legend
======

The legend can be put using ``ax.legend`` in the same way as Matplotlib.
"""
import numpy as np

import matplotlib.pyplot as plt
import mpltern


ax = plt.subplot(projection="ternary")

np.random.seed(19680801)
for i in range(4):
    t, l, r = np.random.dirichlet(alpha=(2.0, 2.0, 2.0), size=10).T
    ax.scatter(t, l, r, alpha=0.5, label=i)

ax.legend()

plt.show()
