#############
Release notes
#############

mpltern 0.4.0
=============

**Matplotlib 3.4.0-3.6.x**

``ax.axline``
-------------

.. |ax.axline| replace:: ``ax.axline``
.. _ax.axline: https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.axline.html

.. |matplotlib330| replace:: ``matplotlib>=3.3.0``
.. _matplotlib330: https://matplotlib.org/stable/users/prev_whats_new/whats_new_3.3.0.html#new-axes-axline-method

|ax.axline|_ can now be used for |matplotlib330|_ and mpltern.
See `gallery <https://mpltern.readthedocs.io/en/latest/gallery/intermediate/axline.html>`__.

``tight_layout`` and ``constrained_layout``
-------------------------------------------

Previously ``tight_layout`` and ``constrained_layout`` did not work as
expected, which is fixed in mpltern 0.4.0.

No overlaps between titles and ternary axes
-------------------------------------------

As done in Matplotlib.

Removal of ``opposite_ticks``
-----------------------------

Instead, ``ax.taxis.set_ticks_position`` and ``ax.taxis.set_label_position``
etc. should be used explicitly.
See `gallery <https://mpltern.readthedocs.io/en/latest/gallery/axis_and_tick/tick_position.html>`__.

Drop support of ``python<3.7`` and ``matplotlib<3.4.0``
-------------------------------------------------------

Python 3.6 is not maintained anymore.
With Python 3.7, Matplotlib 3.4.0 is available.

mpltern 0.3.5
=============

**Matplotlib 3.2.0-3.6.x**

mpltern 0.3.4
=============

**Matplotlib 3.2.0-3.5.x**

While essentially mpltern still works with Matplotlib 3.1.1, I got difficulty
to make it pass the tests and therefore dropped the support.

mpltern 0.3.3
=============

**Matplotlib 3.1.1-3.4.x**

mpltern 0.3.2
=============

**Matplotlib 3.1.1-3.3.x**

Update for conda-forge

mpltern 0.3.1
===============

**Matplotlib 3.1.1-3.3.x**

mpltern 0.3.0
=============

**Matplotlib 3.1.1-3.2.x**

The tick-label rotation in mpltern relies on the rotation of the ``Text``
object in Matplotlib.
In Matplotlib 3.0 or lower, however, there was a bug for the ``Text`` rotation
in case ``va=='center_baseline'`` and ``rotation_mode=='anchor'``
(https://github.com/matplotlib/matplotlib/issues/13028).
If these Matplotlib versions are used, tick-label positions are not as
expected.
**When using mpltern, therefore, it is strongly discouraged to use these old
Matplotlib versions and instead suggested to use higher versions.**
I however also have to note that Matplotlib 3.1 may also have other serious
bugs (e.g. https://github.com/matplotlib/matplotlib/issues/14751).
Until the versions where both the bugs are fixed, the users of mpltern have to
compromise with these issues.
