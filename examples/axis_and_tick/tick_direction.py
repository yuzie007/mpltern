"""
==============
Tick direction
==============

Tick direction can be changed via
`ax.tick_params(direction={'in', 'out', 'inout'})`.
"""
import matplotlib.pyplot as plt
import mpltern

fig = plt.figure(figsize=(14.4, 4.8))
fig.subplots_adjust(left=0.075, right=0.925, wspace=0.3)

ax = fig.add_subplot(131, projection='ternary')
ax.tick_params(direction='in')
ax.set_title("ax.tick_params(direction='in')", pad=36)

ax = fig.add_subplot(132, projection='ternary')
ax.tick_params(direction='out')
ax.set_title("ax.tick_params(direction='out')", pad=36)

ax = fig.add_subplot(133, projection='ternary')
ax.tick_params(direction='inout')
ax.set_title("ax.tick_params(direction='inout')", pad=36)

plt.show()
