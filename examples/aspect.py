"""
======
Aspect
======

The triangle can be scaled by `ax.set_aspect`.
For more general triangles, use ``rotation`` and/or ``corners``.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


fig = plt.figure()

ax = fig.add_subplot(111, projection='ternary')
ax.plot(*get_spiral())

ax.set_aspect(1.5)

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

plt.show()
