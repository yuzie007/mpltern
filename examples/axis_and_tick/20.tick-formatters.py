"""
===============
Tick formatters
===============

.. |PercentFormatter| replace:: ``PercentFormatter``
.. _PercentFormatter: https://matplotlib.org/stable/api/ticker_api.html#matplotlib.ticker.PercentFormatter

`Tick formatters can be given in the same way as Matplotlib
<https://matplotlib.org/stable/gallery/ticks/tick-formatters.html>`__.
Among available formatters, |PercentFormatter|_ may be particularly useful for
ternary plots.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
import mpltern

ternary_sum = 100.0

ax = plt.subplot(projection="ternary", ternary_sum=ternary_sum)

np.random.seed(19680801)
t, l, r = ternary_sum * np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=128).T

ax.scatter(t, l, r, s=64.0, c="none", edgecolors="C0")

ax.set_tlabel("$x_1$")
ax.set_llabel("$x_2$")
ax.set_rlabel("$x_3$")

ax.taxis.set_major_formatter(PercentFormatter())
ax.laxis.set_major_formatter(PercentFormatter())
ax.raxis.set_major_formatter(PercentFormatter())

plt.show()
