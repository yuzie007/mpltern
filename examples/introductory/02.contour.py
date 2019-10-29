"""
=======
Contour
=======

Contour plots can be done using ``ax.tricontour`` or ``ax.tricontourf``.
"""
import numpy as np

import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_shanon_entropies

t, l, r, v = get_shanon_entropies()

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(left=0.075, right=0.85, wspace=0.3)

pad_title = 36

# These values are for controlling the color-bar scale, and here they are
# explicitly given just to make the same color-bar scale for all the plots.
# In general, you may not need to explicitly specify them.
vmin = 0.0
vmax = 1.2
levels = np.linspace(vmin, vmax, 7)

ax = fig.add_subplot(1, 2, 1, projection='ternary')
cs = ax.tricontour(t, l, r, v, levels=levels)
ax.clabel(cs)
ax.set_title("tricontour", pad=pad_title)

cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
colorbar = fig.colorbar(cs, cax=cax)
colorbar.set_label('Entropy', rotation=270, va='baseline')

ax = fig.add_subplot(1, 2, 2, projection='ternary')
cs = ax.tricontourf(t, l, r, v, levels=levels)
ax.set_title("tricontourf", pad=pad_title)

cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
colorbar = fig.colorbar(cs, cax=cax)
colorbar.set_label('Entropy', rotation=270, va='baseline')

plt.show()
