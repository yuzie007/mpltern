"""
==============
Ternary limits
==============

We can limit the ranges of ternary axes.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


ax = plt.subplot(projection='ternary')

ax.plot(*get_spiral())

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

# Using ``ternary_lim``, you can limit the range of ternary axes.
# Be sure about the consistency; the limit values must satisfy:
# tmax + lmin + rmin = tmin + lmax + rmin = tmin + lmin + rmax = ternary_scale
ax.set_ternary_lim(
    0.1, 0.5,  # tmin, tmax
    0.2, 0.6,  # lmin, lmax
    0.3, 0.7,  # rmin, rmax
)

# You can also use ``ternary_min`` and ``ternary_max`` as follows, where you do
# not have to care the consistency above.
# ax.set_ternary_min(0.1, 0.2, 0.3)
# ax.set_ternary_max(0.5, 0.6, 0.7)

plt.show()
