"""
==================
Arbitrary triangle
==================

You can make a ternary plot on an triangle with arbitrary shape.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


corners = ((0.0, 0.0), (0.5, 0.5), (-0.5, 1.0))
ax = plt.subplot(projection='ternary', corners=corners)

ax.plot(*get_spiral())

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

ax.grid()

plt.show()
