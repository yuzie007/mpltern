====================
Supported Matplotlib
====================

- mpltern 0.3.0: Matplotlib 3.1.1+

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

- mpltern 0.3.4: Matplotlib 3.2.0+

  While essentially mpltern still works with Matplotlib 3.1.1, I got difficulty
  to make it pass the tests and therefore dropped the support.
