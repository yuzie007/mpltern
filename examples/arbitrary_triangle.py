"""
==================
Arbitrary triangle
==================

You can make a ternary plot on an triangle with arbitrary shape.
"""
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral


fig = plt.figure()

# Triangle corners in the square of ((0, 0), (1, 0), (1, 1), (0, 1))
corners = ((0.5, 0.0), (1.0, 0.5), (0.0, 1.0))
ax = fig.add_subplot(projection='ternary', corners=corners)

ax.plot(*get_spiral())

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

ax.grid()

plt.show()
