import matplotlib.pyplot as plt
import mpltern

ax = plt.subplot(projection='ternary')

from mpltern.ternary.datasets import get_spiral

t, l, r = get_spiral()
ax.plot(t, l, r)
plt.show()

ax = plt.subplot(projection='ternary')

from mpltern.ternary.datasets import get_shanon_entropies

t, l, r, v = get_shanon_entropies()
ax.tricontourf(t, l, r, v)
plt.show()
# plt.savefig('basic_2.svg', transparent=True)
