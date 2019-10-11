"""
===========================
Tick labels inside triangle
===========================

You can put tick labels inside triangle in the `manual` mode for tick labels.

"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401


fig = plt.figure()
ax = fig.add_subplot(projection='ternary')

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

ax.grid()

ax.tick_params(tick1On=False, tick2On=False)

# By setting `labelrotation='manual'`, automatic rotation and alignment for
# tick labels are prohibited. Instead, you can pass properties for tick labels
# as a dictionary.
kwargs = {'y': 0.5, 'ha': 'center', 'va': 'center', 'rotation_mode': 'anchor'}
tkwargs = {'rotation':  0.0, 'transform': ax.get_taxis_transform()}
lkwargs = {'rotation':-60.0, 'transform': ax.get_laxis_transform()}
rkwargs = {'rotation': 60.0, 'transform': ax.get_raxis_transform()}
tkwargs.update(kwargs)
lkwargs.update(kwargs)
rkwargs.update(kwargs)
ax.taxis.set_tick_params(labelrotation=('manual', tkwargs))
ax.laxis.set_tick_params(labelrotation=('manual', lkwargs))
ax.raxis.set_tick_params(labelrotation=('manual', rkwargs))

plt.show()
