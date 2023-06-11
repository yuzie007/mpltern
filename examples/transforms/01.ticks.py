"""
=====
Ticks
=====

In mpltern, tick markers, tick labels, and grid lines are plotted based on
`ax.get_{t,l,r}axis_transform()` like `ax.get_{x,y}axis_transform()` in
Matplotlib.

For `ax.get_taxis_transform()`, for example, the first coordinate is for the
t-axis values. For the second coordinate, 0 and 1 corresponds to the
`"tick1"` and the `"tick2"` positions, respectively.
Therefore, for the t-axis value of *t*, the tick-marker positions of `"tick1"`
and `"tick2"` are given by (*t*, 0) and (*t*, 1), respectively, and the grid
line spans between (*t*, 0) and (*t*, 1).

Using these transforms, we can e.g. plot the region where the ratio of *l* and
*r* is in a certain range in a bit sementic way as follows.
"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401

ax = plt.subplot(projection="ternary", ternary_sum=100.0)

x0 = 0.0
x1 = 100.0

ax.plot([x0, x1], [0.5, 0.5], transform=ax.get_taxis_transform())
ax.plot([x0, x1], [0.5, 0.5], transform=ax.get_laxis_transform())
ax.plot([x0, x1], [0.5, 0.5], transform=ax.get_raxis_transform())

y = [0.4, 0.6]

ax.fill_betweenx(y, x0, x1, alpha=0.2, transform=ax.get_taxis_transform())
ax.fill_betweenx(y, x0, x1, alpha=0.2, transform=ax.get_laxis_transform())
ax.fill_betweenx(y, x0, x1, alpha=0.2, transform=ax.get_raxis_transform())

plt.show()
