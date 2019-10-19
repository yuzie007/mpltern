import matplotlib.pyplot as plt
import mpltern

ax = plt.subplot(projection='ternary')

from mpltern.ternary.datasets import get_spiral

t, l, r = get_spiral()
ax.plot(t, l, r)
plt.show()
# plt.savefig('basic_usage.svg', transparent=True)
