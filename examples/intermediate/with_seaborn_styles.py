"""
============
Style sheets
============

`You can use style sheets in the same way as Matplotlib.
<https://matplotlib.org/stable/tutorials/introductory/customizing.html
#using-style-sheets>`__
This applies also for the style sheets of third-party packages like
`seaborn <https://seaborn.pydata.org/generated/seaborn.set_style.html>`__.
"""
import matplotlib.pyplot as plt
from mpltern.datasets import get_spiral

# %%

plt.style.use("ggplot")

ax = plt.subplot(projection="ternary")

ax.plot(*get_spiral())

ax.set_tlabel("Top")
ax.set_llabel("Left")
ax.set_rlabel("Right")

plt.show()

# %%

plt.style.use("dark_background")

ax = plt.subplot(projection="ternary")

ax.plot(*get_spiral())

ax.set_tlabel("Top")
ax.set_llabel("Left")
ax.set_rlabel("Right")

plt.show()
