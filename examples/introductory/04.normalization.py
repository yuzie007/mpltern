"""
=============
Normalization
=============

The normalization constant of ternary plots can be modified using ``constant``.

.. note::
    The ternary data are automatically normalized with a few exceptions.
    See details in :doc:`../../conventions`.
"""
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral


fig = plt.figure()
ax = fig.add_subplot(projection='ternary', constant=100.0)
t, l, r = get_spiral()
ax.plot(t, l, r)  # Data are automatically normalized by `constant`.
plt.show()
