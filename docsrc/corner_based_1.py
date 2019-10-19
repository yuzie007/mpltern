import matplotlib.pyplot as plt
import mpltern  # noqa: F401


fig = plt.figure(figsize=(10.8, 4.0))
fig.subplots_adjust(
    left=0.075, right=0.925, bottom=0.15, top=0.9, wspace=0.5)

# Top axis

ax = fig.add_subplot(131, projection='ternary')
ax.scatter(0.6, 0.2, 0.2, c='C3', zorder=10)

ax.set_tlabel('Top')
ax.taxis.label.set_color('C0')

ax.laxis.set_ticklabels([])
ax.raxis.set_ticklabels([])

ax.grid()

ax.taxis.set_tick_params(colors='C0', grid_color='C0', grid_linewidth=2.4)

# Left axis

ax = fig.add_subplot(132, projection='ternary')
ax.scatter(0.6, 0.2, 0.2, c='C3', zorder=10)

ax.set_llabel('Left')
ax.laxis.label.set_color('C1')

ax.raxis.set_ticklabels([])
ax.taxis.set_ticklabels([])

ax.grid()

ax.laxis.set_tick_params(colors='C1', grid_color='C1', grid_linewidth=2.4)

# Right axis

ax = fig.add_subplot(133, projection='ternary')
ax.scatter(0.6, 0.2, 0.2, c='C3', zorder=10)

ax.set_rlabel('Right')
ax.raxis.label.set_color('C2')

ax.taxis.set_ticklabels([])
ax.laxis.set_ticklabels([])

ax.grid()

ax.raxis.set_tick_params(colors='C2', grid_color='C2', grid_linewidth=2.4)

fig.suptitle('Corner-based perspective')

fig.savefig('corner_based_1.svg')
