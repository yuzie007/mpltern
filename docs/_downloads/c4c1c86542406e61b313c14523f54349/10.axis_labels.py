"""
===========
Axis labels
===========

Axis labels can be given using e.g. ``ax.set_tlabel``.
For more detailed control, see :ref:`sphx_glr_gallery_axis_and_tick`.
"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401


ax = plt.subplot(projection='ternary')

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

plt.show()
