"""
================================
Normalization by negative values
================================

You can give negative values to normalize ternary plots.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


ax = plt.subplot(projection='ternary', ternary_scale=-1.0)

ax.plot(*get_spiral())

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

plt.show()
