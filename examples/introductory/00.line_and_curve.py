"""
==============
Line and curve
==============

Lines and curves can be put using ``ax.plot`` in the same way as Matplotlib.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


ax = plt.subplot(projection='ternary')

ax.plot([0.8, 0.6], [0.1, 0.2], [0.1, 0.2])
ax.plot([0.1, 0.2], [0.8, 0.6], [0.1, 0.2], marker='o')
ax.plot([0.1, 0.2], [0.1, 0.2], [0.8, 0.6], ls=':', marker='s', mfc='none')

t, l, r = get_spiral()
ax.plot(t, l, r, color='k')

plt.show()
