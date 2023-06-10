"""
=================
Triangular limits
=================

Suppose we would like to crop or expand the following gray-shaded region.

.. plot::
    :context: reset
    :include-source: false

    import matplotlib.pyplot as plt
    from mpltern.datasets import get_spiral

    ax = plt.subplot(projection='ternary')
    ax.plot(*get_spiral(), color="k")
    ax.fill([0.5, 0.1, 0.1], [0.2, 0.6, 0.2], [0.3, 0.3, 0.7], color="0.6")

    ax.set_tlabel("T")
    ax.set_llabel("L")
    ax.set_rlabel("R")

The region is defined as the intersect of :math:`t \\in [0.1, 0.5]`,
:math:`l \\in [0.2, 0.6]`, :math:`r \\in [0.3, 0.7]`.

.. plot::
    :context:
    :include-source: false

    ax.axtspan(0.1, 0.5, color="C0", fc="none", hatch="....")
    ax.axlspan(0.2, 0.6, color="C1", fc="none", hatch="....")
    ax.axrspan(0.3, 0.7, color="C2", fc="none", hatch="....")
"""
# %%
# To do this, we can use one of the following approaches.
#
# 1. `set_ternary_lim`
# 2. `set_ternary_min` and `set_ternary_max`
# 3. `set_tlim`, `set_llim`, `set_rlim`
#
# Using `set_ternary_lim`, we explicitly specify the min and the max values
# for all the ternary axes.
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral

ax = plt.subplot(projection='ternary')
ax.plot(*get_spiral(), color="k")
ax.set_ternary_lim(
    0.1, 0.5,  # tmin, tmax
    0.2, 0.6,  # lmin, lmax
    0.3, 0.7,  # rmin, rmax
)
# %%
# We can also use `ternary_min` and `ternary_max`. The max and the min values
# of the ternary axes are automatically determined to have a triangle region.
ax = plt.subplot(projection='ternary')
ax.plot(*get_spiral(), color="k")
ax.set_ternary_min(0.1, 0.2, 0.3)
# %%
ax = plt.subplot(projection='ternary')
ax.plot(*get_spiral(), color="k")
ax.set_ternary_max(0.5, 0.6, 0.7)
# %%
# The last way is to specify the min and the max values of each ternary axis
# one by one.
ax = plt.subplot(projection='ternary')
ax.plot(*get_spiral(), color="k")
ax.set_tlim(0.1, 0.5)
ax.set_llim(0.2, 0.6)
ax.set_rlim(0.3, 0.7)
