"""
=================
Arrows along axes
=================

Arrows along the axes can be put in barycentric coordinates using transforms
for ``TernaryAxes`` in combination with ``FancyArrowPatch``.
"""
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import ArrowStyle, FancyArrowPatch
import mpltern  # noqa: F401

ax = plt.subplot(projection='ternary')

arrowstyle = ArrowStyle('simple', head_length=10, head_width=5)
kwargs_arrow = {
    'transform': ax.transAxes,  # Used with ``ax.transAxesProjection``
    'arrowstyle': arrowstyle,
    'linewidth': 1,
    'clip_on': False,  # To plot arrows outside triangle
    'zorder': -10,  # Very low value not to hide e.g. tick labels.
}

# Start of arrows in barycentric coordinates.
ta = np.array([ 0.0, -0.1,  1.1])
la = np.array([ 1.1,  0.0, -0.1])
ra = np.array([-0.1,  1.1,  0.0])

# End of arrows in barycentric coordinates.
tb = np.array([ 1.0, -0.1,  0.1])
lb = np.array([ 0.1,  1.0, -0.1])
rb = np.array([-0.1,  0.1,  1.0])

# This transforms the above barycentric coordinates to the original Axes
# coordinates. In combination with ``ax.transAxes``, we can plot arrows fixed
# to the Axes coordinates.
f = ax.transAxesProjection.transform

tarrow = FancyArrowPatch(f(ta), f(tb), ec='C0', fc='C0', **kwargs_arrow)
larrow = FancyArrowPatch(f(la), f(lb), ec='C1', fc='C1', **kwargs_arrow)
rarrow = FancyArrowPatch(f(ra), f(rb), ec='C2', fc='C2', **kwargs_arrow)
ax.add_patch(tarrow)
ax.add_patch(larrow)
ax.add_patch(rarrow)

# To put the axis-labels at the positions consistent with the arrows above, it
# may be better to put the axis-label-text directly as follows rather than
# using e.g.  ax.set_tlabel.
kwargs_label = {
    'transform': ax.transTernaryAxes,
    'backgroundcolor': 'w',
    'ha': 'center',
    'va': 'center',
    'rotation_mode': 'anchor',
    'zorder': -9,  # A bit higher on arrows, but still lower than others.
}

# Put axis-labels on the midpoints of arrows.
tpos = (ta + tb) * 0.5
lpos = (la + lb) * 0.5
rpos = (ra + rb) * 0.5

ax.text(*tpos, 'Top'  , color='C0', rotation=-60, **kwargs_label)
ax.text(*lpos, 'Left' , color='C1', rotation= 60, **kwargs_label)
ax.text(*rpos, 'Right', color='C2', rotation=  0, **kwargs_label)

plt.show()
