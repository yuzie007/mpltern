"""
=============
Tick locators
=============

`Tick locators can be given both for major and minor ticks in the same way as
Matplotlib <https://matplotlib.org/stable/gallery/ticks/tick-locators.html>`__.
Gridlines for minor ticks can be also plotted.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import mpltern

ax = plt.subplot(projection="ternary")

np.random.seed(19680801)
t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=128).T

ax.scatter(t, l, r, s=64.0, c="C1", edgecolors="k", alpha=0.6)

ax.set_tlabel("$x_1$")
ax.set_llabel("$x_2$")
ax.set_rlabel("$x_3$")

ax.taxis.set_major_locator(MultipleLocator(0.25))
ax.laxis.set_major_locator(MultipleLocator(0.20))
ax.raxis.set_major_locator(MultipleLocator(0.10))

ax.laxis.set_minor_locator(MultipleLocator(0.1))
ax.raxis.set_minor_locator(AutoMinorLocator(5))

ax.grid(axis='t')
ax.grid(axis='l', which='minor', linestyle='--')
ax.grid(axis='r', which='both', linestyle=':')

plt.show()
