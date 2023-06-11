"""
=============
Tick rotation
=============

Tick rotation can be modified via
`ax.tick_params(labelrotation={'tick', 'axis', 'horizontal'})`.
"""
import matplotlib.pyplot as plt
import mpltern

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(left=0.075, right=0.925, wspace=0.25)

for i, labelrotation in enumerate(["tick", "axis", "horizontal"]):
    ax = fig.add_subplot(1, 3, i + 1, projection='ternary')
    ax.tick_params(labelrotation=labelrotation)
    ax.set_title(f"labelrotation='{labelrotation}'", pad=36)

plt.show()
