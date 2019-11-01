"""
===================
Axis-label rotation
===================

Axis-label rotation can be controlled via e.g.
``ax.taxis.set_label_rotation_mode``.

- ``'axis'``: along the axis opposite to the corner
- ``'horizontal'``: horizontal to the figure

.. Note::
    The ``'manual'`` option is also provided. In this mode, it becomes possible
    to specify the ``Text`` properties like ``horizontalalignment``,
    ``verticalalignment``, and ``rotation`` of axis labels directly,
    which are anymore never modified automatically by mpltern.
"""
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


pad = 42

t, l, r = get_spiral()

fig = plt.figure(figsize=(10.8, 4.8))
fig.subplots_adjust(wspace=0.3)

modes = ['axis', 'horizontal']
for i, mode in enumerate(modes):
    ax = fig.add_subplot(1, 2, i + 1, projection='ternary')

    ax.plot(t, l, r)

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.taxis.set_label_rotation_mode(mode)
    ax.laxis.set_label_rotation_mode(mode)
    ax.raxis.set_label_rotation_mode(mode)

    ax.set_title("label_rotation_mode='{}'".format(mode), pad=pad)

plt.show()
