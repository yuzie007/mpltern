"""
=======
Scatter
=======

Scatter plots can be done using ``ax.scatter``.
"""
import numpy as np

import matplotlib.pyplot as plt
import mpltern


np.random.seed(seed=19)
t0, l0, r0 = np.random.dirichlet(alpha=(2.0, 2.0, 2.0), size=100).T

np.random.seed(seed=68)
t1, l1, r1 = np.random.dirichlet(alpha=(2.0, 2.0, 2.0), size=100).T

dt = t1 - t0
dl = l1 - l0
dr = r1 - r0

length = np.sqrt(dt**2 + dl**2 + dr**2)

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(left=0.075, right=0.85, wspace=0.3)

ax = fig.add_subplot(1, 2, 1, projection="ternary")
pc = ax.scatter(t0, l0, r0)
pc = ax.scatter(t1, l1, r1)

ax = fig.add_subplot(1, 2, 2, projection="ternary")
pc = ax.scatter(t0, l0, r0, c=length)

cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
colorbar = fig.colorbar(pc, cax=cax)
colorbar.set_label("Length", rotation=270, va="baseline")

plt.show()
