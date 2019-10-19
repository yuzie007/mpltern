"""
=================
Triangle rotation
=================

The triangle for a ternary plot can be rotated by `rotation`.
Axis labels, tick labels, and tick markers are also automatically aligned.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


pad = 42

t, l, r = get_spiral()

fig = plt.figure(figsize=(10.8, 8.8))
fig.subplots_adjust(
    left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.5, hspace=0.5)

rotations = range(0, 360, 90)
for i, rotation in enumerate(rotations):
    ax = fig.add_subplot(2, 2, i + 1, projection='ternary', rotation=rotation)

    ax.plot(t, l, r)

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.set_title("rotation={}".format(rotation), pad=pad)

plt.show()
