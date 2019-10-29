"""
=======
Polygon
=======

Polygons in ternary plots can be put using ``ax.fill``.
"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401


ax = plt.subplot(111, projection='ternary')

t = [0.2, 0.4, 0.2]
l = [0.0, 0.2, 0.4]
r = [0.8, 0.4, 0.4]
ax.fill(t, l, r, alpha=0.2)

t = [0.4, 0.6, 0.6, 0.4]
l = [0.2, 0.2, 0.4, 0.4]
r = [0.4, 0.2, 0.0, 0.2]
ax.fill(t, l, r, alpha=0.2)

t = [0.2, 0.4, 0.4, 0.0, 0.0]
l = [0.4, 0.4, 0.6, 1.0, 0.6]
r = [0.4, 0.2, 0.0, 0.0, 0.4]
ax.fill(t, l, r, alpha=0.2)

plt.show()
