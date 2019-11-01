"""
####
Grid
####

The grid along the tick positions can be plotted using ``ax.grid``.
For more detailed control, see :doc:`../advanced/02.minor_ticks`.
"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401


ax = plt.subplot(projection='ternary')

ax.grid()

plt.show()
