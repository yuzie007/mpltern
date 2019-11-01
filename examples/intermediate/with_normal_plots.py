"""
============================
With normal Matplotlib plots
============================

Ternary plots of mpltern can be combined with normal Matplotlib plots very
straightforwardly.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


t, l, r = get_spiral()

fig = plt.figure(figsize=(10.8, 4.8))

# Enough space may need to make the heights of the ternary and the normal plots
# the same.
fig.subplots_adjust(left=0.075, right=0.95)

ax = fig.add_subplot(121, projection='ternary')

ax.plot(t, l, r, 'k')

ax = fig.add_subplot(122)

ax.plot(t)
ax.plot(l)
ax.plot(r)

plt.show()
