"""
=================
Arrows along axes
=================

Arrows along the axes can be put in barycentric coordinates using
`ax.transTernaryAxes`.
This should work as expected also in an interactive mode.
"""
import numpy as np

import matplotlib.pyplot as plt
import mpltern  # noqa: F401

fig = plt.figure()
ax = fig.add_subplot(projection='ternary')

kwargs_arrow = {
    'transform': ax.transTernaryAxes,
    'head_width': 0.02,
    'length_includes_head': True,
    'clip_on': False,  # To plot arrows outside triangle
    'zorder': -10,  # Set very low value not to hide e.g. tick labels.
}

# Origins of the arrows in barycentric coordinates.
to = np.array([ 0.00, -0.10,  1.10])
lo = np.array([ 1.10,  0.00, -0.10])
ro = np.array([-0.10,  1.10,  0.00])

# Lengths of the arrows in barycentric coordinates.
tl = np.array([ 1.0,  0.0, -1.0])
ll = np.array([-1.0,  1.0,  0.0])
rl = np.array([ 0.0, -1.0,  1.0])

ax.arrow(*to, *tl, ec='C0', fc='C0', **kwargs_arrow)
ax.arrow(*lo, *ll, ec='C1', fc='C1', **kwargs_arrow)
ax.arrow(*ro, *rl, ec='C2', fc='C2', **kwargs_arrow)

# # To put the axis-labels at the positions consistent with the arrows above,
# # it may be better to put the axis-label-text directly as follows rather than
# # using e.g.  ax.set_tlabel.
kwargs_label = {
    'transform': ax.transTernaryAxes,
    'backgroundcolor': 'w',
    'ha': 'center',
    'va': 'center',
    'rotation_mode': 'anchor',
    'zorder': -9,  # A bit higher on arrows, but still lower than others.
}

# Put axis-labels on the midpoints of arrows.
tpos = to + 0.5 * tl
lpos = lo + 0.5 * ll
rpos = ro + 0.5 * rl

ax.text(*tpos, 'Top'  , color='C0', rotation=-60, **kwargs_label)
ax.text(*lpos, 'Left' , color='C1', rotation= 60, **kwargs_label)
ax.text(*rpos, 'Right', color='C2', rotation=  0, **kwargs_label)

ax.tick_params(labelrotation='tick')

plt.show()
