"""
================
Hexagonal limits
================

.. note::

    Available with ``mpltern>=1.0.0``

Suppose we would like to crop or expand the following gray-shaded region.

.. plot::
    :context: reset
    :include-source: false

    import numpy as np
    import matplotlib.pyplot as plt
    from mpltern.datasets import get_spiral

    ax = plt.subplot(projection='ternary')
    ax.plot(*get_spiral(), color="k")
    points = np.array([
        [0.7, 0.1, 0.2],
        [0.7, 0.2, 0.1],
        [0.2, 0.7, 0.1],
        [0.1, 0.7, 0.2],
        [0.1, 0.2, 0.7],
        [0.2, 0.1, 0.7],
    ])
    ax.fill(points[:, 0], points[:, 1], points[:, 2], color="0.6")

    ax.set_tlabel("T")
    ax.set_llabel("L")
    ax.set_rlabel("R")

The region is defined as the intersect of :math:`t \\in [0.1, 0.7]`,
:math:`l \\in [0.1, 0.7]`, :math:`r \\in [0.1, 0.7]`.

.. plot::
    :context:
    :include-source: false

    ax.axtspan(0.1, 0.7, color="C0", fc="none", hatch="....")
    ax.axlspan(0.1, 0.7, color="C1", fc="none", hatch="....")
    ax.axrspan(0.1, 0.7, color="C2", fc="none", hatch="....")
"""
# %%
# Using `set_ternary_lim`, we explicitly specify the min and the max values
# for all the ternary axes.
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral

ax = plt.subplot(projection='ternary')

ax.plot(*get_spiral(), color="k")

ax.set_ternary_lim(
    0.1, 0.7,  # tmin, tmax
    0.1, 0.7,  # lmin, lmax
    0.1, 0.7,  # rmin, rmax
)

ax.set_tlabel("T")
ax.set_llabel("L")
ax.set_rlabel("R")

# For a hexagonal plotting region, it may be better to put the axis labels on
# the sides (either "tick1" or "tick2") rather than the default "corner" to
# avoid confusion.
ax.taxis.set_label_position("tick1")
ax.laxis.set_label_position("tick1")
ax.raxis.set_label_position("tick1")

plt.show()
# %%
# We can also set the min and the max values of each ternary axis one by one.
ax = plt.subplot(projection='ternary')

ax.plot(*get_spiral(), color="k")

ax.set_tlim(0.1, 0.7)
ax.set_llim(0.1, 0.7)
ax.set_rlim(0.1, 0.7)

plt.show()
