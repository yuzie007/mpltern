"""
==============
Tick direction
==============

Tick direction can be modified via
`ax.tick_params(direction={'in', 'out', 'inout'})`.
"""
import matplotlib.pyplot as plt
import mpltern

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(left=0.075, right=0.925, wspace=0.25)

for i, direction in enumerate(["in", "out", "inout"]):
    ax = fig.add_subplot(1, 3, i + 1, projection='ternary')
    ax.tick_params(direction=direction)
    ax.set_title(f"ax.tick_params(direction='{direction}')", pad=36)

plt.show()
