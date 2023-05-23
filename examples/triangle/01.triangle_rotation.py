"""
=================
Triangle rotation
=================

The triangle for a ternary plot can be rotated by `rotation`.
Axis labels, tick labels, and tick markers are also automatically aligned.
"""
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral


t, l, r = get_spiral()

fig = plt.figure(figsize=(10.8, 8.8))
fig.subplots_adjust(
    left=0.1,
    right=0.9,
    hspace=0.75,
)

rotations = range(0, 360, 90)
for i, rotation in enumerate(rotations):
    ax = fig.add_subplot(2, 2, i + 1, projection='ternary', rotation=rotation)

    ax.plot(t, l, r)

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.set_title(f"rotation={rotation}")

plt.show()
