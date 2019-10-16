"""
===========================
Tick labels inside triangle
===========================

You can put tick labels inside triangle by setting ``labelrotation=manual`` and
then specifying appropriate ``Text`` properties as follows.

.. note::

    This works also in interactive modes. This is achieved by overriding
    ``Axis._copy_tick_props`` also to update the *y* coordinate.
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

# By setting ``labelrotation='manual'``, automatic rotation and alignment for
# tick labels are prohibited.
ax.taxis.set_tick_params(labelrotation=('manual',   0.0))
ax.laxis.set_tick_params(labelrotation=('manual', -60.0))
ax.raxis.set_tick_params(labelrotation=('manual',  60.0))

# Then, ``Text`` properties you like can be passed directly by ``update``.
kwargs = {'y': 0.5, 'ha': 'center', 'va': 'center', 'rotation_mode': 'anchor'}
tkwargs = {'transform': ax.get_taxis_transform()}
lkwargs = {'transform': ax.get_laxis_transform()}
rkwargs = {'transform': ax.get_raxis_transform()}
tkwargs.update(kwargs)
lkwargs.update(kwargs)
rkwargs.update(kwargs)
[text.update(tkwargs) for text in ax.taxis.get_ticklabels()]
[text.update(lkwargs) for text in ax.laxis.get_ticklabels()]
[text.update(rkwargs) for text in ax.raxis.get_ticklabels()]

plt.show()
