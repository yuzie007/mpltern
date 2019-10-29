"""
======
Aspect
======

The triangle aspect can be modified by `ax.set_aspect`.
For more general triangles, use ``rotation`` and/or ``corners``.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


ax = plt.subplot(projection='ternary')
ax.plot(*get_spiral())

ax.set_aspect(1.5)

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

plt.show()
