"""
====
Span
====

A line or a band horizontal to an ternary axis can be plotted by the commands
``axtline``, ``axlline``, ``axrline``, ``axtspan``, ``axlspan``, ``axrspan``.
"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401


ax = plt.subplot(projection='ternary')

ax.set_tlabel('Top')
ax.set_llabel('Left')
ax.set_rlabel('Right')

ax.axtline(0.2, c='C0')
ax.axlline(0.3, c='C1')
ax.axrline(0.4, c='C2')

ax.axtspan(0.3, 0.5, fc='C0', alpha=0.2)
ax.axlspan(0.4, 0.6, fc='C1', alpha=0.2)
ax.axrspan(0.5, 0.7, fc='C2', alpha=0.2)

plt.show()
