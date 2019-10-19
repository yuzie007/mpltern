"""
===================
Axis-label rotation
===================

The rotation of axis labels can be controlled via e.g.
``ax.taxis.set_label_rotation_mode``.

- ``'axis'``: along the axis opposite to the corner
- ``'horizontal'``: horizontal to the figure

.. Note::
    The ``'manual'`` option is also provided. In this mode, it becomes possible
    to specify the ``Text`` properties like ``horizontalalignment``,
    ``verticalalignment``, and ``rotation`` of axis labels directly,
    which are anymore never modified automatically by Mpltern.
"""

import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


pad = 42

t, l, r = get_spiral()

fig = plt.figure(figsize=(10.8, 8.8))
fig.subplots_adjust(
    left=0.1, right=0.9, bottom=0.1, top=0.9, wspace=0.5, hspace=0.5)

#

ax = fig.add_subplot(2, 2, 1, projection='ternary')
ax.plot(t, l, r)

title = "label_position='corner', label_rotation_mode='axis'"
ax.set_title(title, pad=pad)

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

#

ax = fig.add_subplot(2, 2, 2, projection='ternary')
ax.plot(t, l, r)

title = "label_position='corner', label_rotation_mode='horizontal'"
ax.set_title(title, pad=pad)

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

ax.taxis.set_label_rotation_mode('horizontal')
ax.laxis.set_label_rotation_mode('horizontal')
ax.raxis.set_label_rotation_mode('horizontal')

#

ax = fig.add_subplot(2, 2, 3, projection='ternary')
ax.plot(t, l, r)

title = "label_position='tick1', label_rotation_mode='axis'"
ax.set_title(title, pad=pad)

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

ax.taxis.set_label_position('tick1')
ax.laxis.set_label_position('tick1')
ax.raxis.set_label_position('tick1')

#

ax = fig.add_subplot(2, 2, 4, projection='ternary')
ax.plot(t, l, r)

title = "label_position='tick1', label_rotation_mode='horizontal'"
ax.set_title(title, pad=pad)

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

ax.taxis.set_label_position('tick1')
ax.laxis.set_label_position('tick1')
ax.raxis.set_label_position('tick1')

ax.taxis.set_label_rotation_mode('horizontal')
ax.laxis.set_label_rotation_mode('horizontal')
ax.raxis.set_label_rotation_mode('horizontal')

#

plt.show()
