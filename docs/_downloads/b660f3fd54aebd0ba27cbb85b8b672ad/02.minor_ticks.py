"""
===========
Minor ticks
===========

Minor ticks can be given using Matplotlib locators.
Gridlines for minor ticks can be also plotted.
"""
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
import mpltern  # noqa: F401


ax = plt.subplot(projection='ternary')

ax.laxis.set_minor_locator(MultipleLocator(0.1))
ax.raxis.set_minor_locator(AutoMinorLocator(5))

ax.grid(axis='t')
ax.grid(axis='l', which='minor', linestyle='--')
ax.grid(axis='r', which='both', linestyle=':')

plt.show()
