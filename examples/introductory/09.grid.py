"""
####
Grid
####

The grid along the tick positions can be plotted using ``ax.grid``. See also
:doc:`tick locators <../axis_and_tick/21.tick-locators>` for more controls.
"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401


ax = plt.subplot(projection='ternary')

ax.grid()

plt.show()
