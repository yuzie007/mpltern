"""
=============
Tick rotation
=============

Tick rotation can be changed via
`ax.tick_params(labelrotation={'tick', 'axis', 'horizontal'})`.
"""
import matplotlib.pyplot as plt
import mpltern

fig = plt.figure(figsize=(14.4, 4.8))
fig.subplots_adjust(left=0.075, right=0.925, wspace=0.3)

ax = fig.add_subplot(131, projection='ternary')
ax.tick_params(labelrotation='tick')
ax.set_title("labelrotation='tick'", pad=36)

ax = fig.add_subplot(132, projection='ternary')
ax.tick_params(labelrotation='axis')
ax.set_title("labelrotation='axis'", pad=36)

ax = fig.add_subplot(133, projection='ternary')
ax.tick_params(labelrotation='horizontal')
ax.set_title("labelrotation='horizontal'", pad=36)

plt.show()
