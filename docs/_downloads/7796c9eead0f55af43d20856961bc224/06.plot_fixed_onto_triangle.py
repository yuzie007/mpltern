"""
========================
Plot fixed onto triangle
========================

You can plot onto the fixed positions of the triangle by specifying
`tranform=ax.transTernaryAxes`.
This may be particularly useful for some cases in interactive modes.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


t, l, r = get_spiral()
c = 1.0 / 3.0

ax = plt.subplot(projection='ternary')
ax.set_ternary_min(0.1, 0.2, 0.3)

ax.plot(t, l, r)
ax.text(c, c, c, 'Data', ha='center')

ax.plot(t, l, r, transform=ax.transTernaryAxes)
ax.text(c, c, c, 'Axes', ha='center', transform=ax.transTernaryAxes)

plt.show()
