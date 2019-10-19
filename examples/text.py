"""
====
Text
====

Texts in ternary plots can be put by ``ax.text``.
"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401

ax = plt.subplot(projection='ternary')

c = 1.0 / 3.0
ax.text(c, c, c, 'center', ha='center', va='center')

plt.show()
