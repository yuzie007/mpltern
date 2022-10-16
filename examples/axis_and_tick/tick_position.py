"""
=============
Tick position
=============

Tick position can be controlled via e.g.
``ax.taxis.set_ticks_position``.

- ``'tick1'``: side for tick1
- ``'tick2'``: side for tick2
- ``'both'``: both side

When the axis labels are on the sides, e.g. ``ax.taxis.set_label_position``
should also be used.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


t, l, r = get_spiral()

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(wspace=0.3)

positions = ['tick1', 'tick2']
for i, position in enumerate(positions):
    ax = fig.add_subplot(1, 2, i + 1, projection='ternary')

    ax.plot(t, l, r)

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.taxis.set_ticks_position(position)
    ax.laxis.set_ticks_position(position)
    ax.raxis.set_ticks_position(position)

    ax.taxis.set_label_position(position)
    ax.laxis.set_label_position(position)
    ax.raxis.set_label_position(position)

    ax.set_title(f"position='{position}'", pad=42)

plt.show()
