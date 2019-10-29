"""
=============
Normalization
=============

The normalization of ternary plots can be modified using ``ternary_scale``.

.. note::
    The ternary data are automatically normalized with a few exceptions.
    See details in :doc:`../../conventions`.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


fig = plt.figure()

ternary_scale = 0.5
ax = fig.add_subplot(projection='ternary', ternary_scale=ternary_scale)

t, l, r = get_spiral()

ax.plot(t, l, r)  # Data are automatically normalized by `ternary_scale`.

plt.show()
