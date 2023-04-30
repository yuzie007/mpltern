Axis and Tick
=============

.. |Transform| replace:: ``Transform``
.. _Transform: https://matplotlib.org/stable/tutorials/advanced/transforms_tutorial.html

Mpltern is implemented as a new
`projection <https://matplotlib.org/stable/api/projections_api.html>`__
of Matplotlib.
This is achieved by implementing several new |Transform|_ classes specifically
designed for ternary plots.
This allows us to auto-position tick markers, tick labels, and axis labels with
reasonable paddings consistent with Matplotlib.

The examples below show how to modify positioning of tick markers, tick labels,
and axis labels.
