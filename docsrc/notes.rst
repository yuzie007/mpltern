################################
Notes for mpltern Implementation
################################

This page is rather personal notes of the author and summarizes the things
learned about Matplotlib during the mpltern implementation.

Aims of mpltern
===============

Compared with other Python-based implementations for ternary plots,
mpltern focuses on providing a similar user experience to Matplotlib.
Practically, this aim is hopefully accomplished by:

- Implementation of ``TernaryAxes`` inheriting ``Axes`` of Matplotlib.
    - Components of ``Axes`` like ``Axis`` and ``Tick`` are also overridden as
      ``TernaryAxis`` and ``TernaryTick``, respectively.
- Parameters in ``rcParams`` of Matplotlib rather than hard-coded defaults.
  This also enables us to use seaborn styles with mpltern.
- Employments of new ``transform`` classes useful for ternary plots.
  This particularly makes mpltern work nicely not only in non-interactive modes
  but also in interactive modes.

``Axes``
========

``Axes.plot``
-------------

The first arguments ``x`` and ``y`` are actually positional arguments,
and therefore their order cannot be exchanged.
Following this behavior, also in mpltern,
the order of ``t``, ``l``, ``r`` cannot be exchanged.

``ax.plot`` can run even without any positional arguments.
In this case, a list of no length (``[]``)
is returned.
(see the implementation of
``matplotlib.axes._base._process_plot_var_args.__call__``).

``AxesSubplot``
---------------

The ``AxesSubplot`` class is *dynamically* created by
``matplotlib.axes._subplots.subplot_class_factory``.

In mpltern, ``TernaryAxes`` is defined without the suffix ``Subplot``,
similarly to ``Axes`` in Matplotlib, but if it is created e.g. via
``fig.add_subplot`` it becomes ``TernaryAxesSubplot``.

Registration of a New Projection
================================

In Matplotlib, to use ``Axes3D`` one has to import
``mpl_toolkits.mplot3d.Axes3D``, as described in the
`Matplotlib mplot3d tutorial <https://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html>`_.
In mpltern, however, it is decided NOT to follow this way due to the increase of
the typing effort.
Instead, ``TernaryAxes`` is available by just importing ``mpltern``.
While in most cases mpltern tries to follow the ways of Matplotlib,
this is one of the exceptions.

``Axis``
========

``set_ticks_position``
----------------------

In Matplotlib, ``'default'`` actually does not restore the default positions
of ticks.
This may be due to the compatibility with Matplotlib 1.x.
In mpltern, ``'default'`` is equivalent to ``'tick1'``.

``offsetText``
--------------

When, for example, we have a large *y*-axis values, Matplotlib shows the values
as the differences from the reference value, which is shown at one end.
The ``offsetText`` indicates the text showing this reference value.

Remove round-off
----------------

Before Matplotlib 3.1.0, ``_get_pixel_distance_along_axis`` was used in
``Axis`` classes.
In ``TernaryAxis``, this method had to be overridden.
In Matplotlib 3.1.0, this becomes not necessary thanks to the simplification
and the improvement of consistency
(`#12158 <https://github.com/matplotlib/matplotlib/pull/12158>`_ in Matplotlib).

``TernaryAxis``
---------------

- To be overridden
    - ``update_label_position``
        - The positions of ticks are updated via ``_update_ticks``.

The default ``verticalaligment`` of axis labels in Matplotlib are:

- ``XAxis.label``
    - ``'bottom'``: ``'top'``
    - ``'top'``: ``'baseline'``
- ``YAxis.label``
    - ``'left'``: ``'bottom'``
    - ``'right'``: ``'top'``

The above gives different spaces between tick labels and the axis labels
for the *x* and the *y* axes when tick labels come below the axis label.
In mpltern, ``bottom`` is used by default when the tick labels come below the
axis label.
This is because ``baseline`` and ``top`` apparently give different spaces to
their tick labels if the label text has a descent.

``Tick``
========

Markers
-------

In Matplotlib, ticks are defined as a list of ``Tick`` instances.
Each ``Tick`` corresponds to a value of the corresponding coordinate.
A ``Tick`` has three ``Line2D`` instances to show a tick marker for each side
and a grid and has two ``Text`` instances to show tick labels on both sides.

A tick is shown by a marker.
By default, the tick-maker in Matplotlib is already scaled as

- ``1.0 if self._tickdir in ['in', 'out']``
- ``0.5 if self._tickdir in ['inout']``

and is already rotated by 90 degrees for the ``XTick``.

To make a tilted tick marker, mpltern rotates and scales the default one in the
``TernaryTick._tilt_marker`` method.
When tilting the tick-marker, we must also re-apply the above
rotation and the scaling to it.

``RadialTick`` in ``PolarAxes``
-------------------------------

When a circular sector is drawn, the horizontal and the vertical alignments of
tick labels cannot be modified from outside.

``TernaryTick`` in mpltern
--------------------------

- To be overridden:
    - ``_get_tick1line``, ``_get_tick2line``, ``_get_gridline``
        - ``transform`` of the line must be overridden by the one suitable for
          the corresponding ternary axis.
    - ``update_position``
        - Tick-angles are modified in this method with calling the
          ``_tilt_marker`` method inside.

``fig.colorbar``
================

In ``fig.colorbar`` in Matplotlib, the position of the colorbar does not care
*y*-ticks on the right.
The keywords ``fraction`` and ``pad`` determine the position of the colorbar,
which we specify by hand.
Following to this behavior, mpltern does NOT automatically position the
colorbar but requests users to do by hand.

Interactive Modes
=================

The buttons in the interactive mode call the following methods:

- ``Home``: ``_set_view``
- ``Pan/Zoom``: ``drag_pan``
- ``Zoom-to-rectangle``: ``_set_view_from_bbox``

If you want to scale the axes for ternary plots according to the change of
(``xmin``, ``ymin``, ``xmax``, ``ymax``), these methods should be overridden
to call the rescaling method for the axes of ternary plots
(``_set_ternary_lim_from_xlim_and_ylim``).

If you want to prohibit e.g. ``Zoom-to-rectanble``, you need to override e.g.
``can_zoom`` to return ``False``. (``PolarAxes`` in Matplotlib does this.)

Versioning
==========

The versioning is automatically done using ``versioneer.py``.
To make ``mpltern.__version__`` available, ``versionfile_build`` must be
specified in ``setup.cfg``. Details are found in
https://github.com/warner/python-versioneer/blob/master/INSTALL.md.

Documentation
=============

This summarizes the things learned
about `Sphinx <https://www.sphinx-doc.org/en/master/>`_ and
`Read the Docs <https://docs.readthedocs.io/en/stable/>`_ during the
documentation of mpltern 0.3.1+.

How to redirect to Read the Docs
--------------------------------

The website https://yuzie007.github.io/mpltern is now redirected to
https://mpltern.readthedocs.io following the way in
https://gist.github.com/domenic/1f286d415559b56d725bee51a62c24a7.

How the table of contents displays
----------------------------------

In Sphinx version 2.0+, the TOC taken from "contents" by default.
Read the Docs, in contrast, the home page, which is "index" by default, is
supposed to have ``toctree``, from which the TOC is created.
What I wanted to do is to set "index" as the home page without showing the TOC
explicitly. This can be actually achieved by following
https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html#how-the-table-of-contents-displays.

TODO
====

High
----

Medium
------

- Crosshairs
- Reduce the usages of private methods in Matplotlib

Low
---

- ``annotate``
  (Adequate manipulations for ``xycoords`` and ``textcoords`` are required,
  which is tough for my current time schedule.)
- Isoproportion lines
- ``errorbar``
  (Implementation of error bars along ternary axes?
  The error bars in ternary plots for different axes may be correlated with
  each other.)
- More general (hexagonal) plotting of a part of the triangle
- Parallelogram plots
- Piper diagram
- Triangular and hexagonal binning with values (like `ggtern <http://www.ggtern.com/2017/07/23/version-2-2-1-released/>`_)
- Tie lines
- Log scale
- Scatter Hist (ternary-plot version of `Matplotlib <https://matplotlib.org/gallery/axes_grid1/scatter_hist_locatable_axes.html>`_)
