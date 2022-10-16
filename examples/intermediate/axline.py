"""
======
AxLine
======

An infinitely long straight line can be added using ``ax.axline`` in a similar
way as Matplotlib. This may be helpful, e.g., for adding an isoproportion line.

.. note::

    This is available with ``matplotlib>=3.3``.

Unlike Matplotlib, ``slope`` is the displacement from the first argument and
must be of length 3, whose sum should be zero. The sum of the first argument
and ``slope`` is automatically scaled by ``ternary_scale``.

With ``matplotlib>=3.4``, a keyword argument ``transform`` can be given.
Particularly when ``ax.transTernaryAxes`` is given, a line fixed to the
triangle can be added by giving the first and the second arguments in the
barycentric coordinates.
"""
import matplotlib.pyplot as plt
import mpltern

ax = plt.subplot(projection="ternary")

ax.axline(
    [1.0, 0.0, 0.0],
    [0.0, 0.8, 0.2],
    color="C0",
)
ax.axline(
    [1.0, 0.0, 0.0],
    slope=[-0.2, 0.1, 0.1],
    color="C1",
)
ax.axline(
    [1.0, 0.0, 0.0],
    [0.0, 0.2, 0.8],
    color="C2",
    transform=ax.transTernaryAxes,
)

plt.show()
