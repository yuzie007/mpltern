"""
=============
Normalization
=============

The normalization constant of ternary plots can be modified using
``ternary_sum``.

.. warning::
    Prior to mpltern 1.0.0, the option name was ``ternary_scale``.

.. note::
    The ternary data are automatically normalized with a few exceptions.
    See details in :doc:`../../conventions`.
"""
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral


fig = plt.figure()
ax = fig.add_subplot(projection='ternary', ternary_sum=100.0)
t, l, r = get_spiral()
ax.plot(t, l, r)  # Data are automatically normalized by ``ternary_sum``.
plt.show()
