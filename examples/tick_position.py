"""
=============
Tick position
=============

Tick position can be changed via ``ax.opposite_ticks``.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


pad = 42

t, l, r = get_spiral()

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(wspace=0.3)

bs = [False, True]
for i, b in enumerate(bs):
    ax = fig.add_subplot(1, 2, i + 1, projection='ternary')

    ax.plot(t, l, r)

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.opposite_ticks(b)

    ax.set_title("opposite_ticks({})".format(b), pad=pad)

plt.show()
