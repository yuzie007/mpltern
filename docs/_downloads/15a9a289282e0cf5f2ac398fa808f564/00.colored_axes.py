"""
============
Colored axes
============

You can give a different color for each axis.

"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


fig = plt.figure()
ax = fig.add_subplot(projection='ternary')

ax.plot(*get_spiral(), color='k')

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

ax.grid()

# Color ticks, grids, tick-labels
ax.taxis.set_tick_params(tick2On=True, colors='C0', grid_color='C0')
ax.laxis.set_tick_params(tick2On=True, colors='C1', grid_color='C1')
ax.raxis.set_tick_params(tick2On=True, colors='C2', grid_color='C2')

# Color labels
ax.taxis.label.set_color('C0')
ax.laxis.label.set_color('C1')
ax.raxis.label.set_color('C2')

# Color spines
ax.spines['tside'].set_color('C0')
ax.spines['lside'].set_color('C1')
ax.spines['rside'].set_color('C2')

plt.show()
