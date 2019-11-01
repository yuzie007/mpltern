"""
===================
With seaborn styles
===================

You can use seaborn styles with mpltern in the same way as Matplotlib.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral
import seaborn as sns


sns.set_style('darkgrid')

ax = plt.subplot(projection='ternary')

ax.plot(*get_spiral())

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

plt.show()
