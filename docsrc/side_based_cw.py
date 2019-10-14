import numpy as np

import matplotlib.pyplot as plt
import mpltern


fig = plt.figure(figsize=(10.8, 3.2))
fig.subplots_adjust(
    left=0.075, right=0.925, bottom=0.125, top=0.825, wspace=0.65)

# Top axis

ax = fig.add_subplot(131, projection='ternary')

ax.set_blabel('Right')
ax.baxis.label.set_color('C0')

ax.raxis.set_ticklabels([])
ax.laxis.set_ticklabels([])

ax.grid(True)
ax.grid(axis='b', lw=2.4)

ax.baxis.set_tick_params(colors='C0', grid_color='C0')

ax.opposite_ticks(True)

# Left axis

ax = fig.add_subplot(132, projection='ternary')

ax.set_rlabel('Left')
ax.raxis.label.set_color('C1')

ax.laxis.set_ticklabels([])
ax.baxis.set_ticklabels([])

ax.grid(True)
ax.grid(axis='r', lw=2.4)

ax.raxis.set_tick_params(colors='C1', grid_color='C1')

ax.opposite_ticks(True)

# Right axis

ax = fig.add_subplot(133, projection='ternary')

ax.set_llabel('Bottom')
ax.laxis.label.set_color('C2')

ax.baxis.set_ticklabels([])
ax.raxis.set_ticklabels([])

ax.grid(True)
ax.grid(axis='l', lw=2.4)

ax.laxis.set_tick_params(colors='C2', grid_color='C2')

ax.opposite_ticks(True)

fig.suptitle('Side-based perspective with clockwise ticks')
fig.savefig('side_based_cw.svg')
