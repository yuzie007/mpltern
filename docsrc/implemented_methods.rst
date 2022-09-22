###################
Implemented Methods
###################

The following methods are available, instead of by giving ``x`` and ``y`` as
the first two arguments, by giving ``t``, ``l``, ``r`` as the first three
arguments:

- ``ax.text``
- ``ax.plot``
- ``ax.scatter``
- ``ax.fill``
- ``ax.tricontour``
- ``ax.tricontourf``
- ``ax.tripcolor``
- ``ax.triplot``

.. Note::

    While also available, the followings methods have not supported well yet
    in mpltern.

        - ``ax.hexbin``
        - ``ax.hist2d``

Similarly, the following methods are available by giving,
``t``, ``l``, ``r``, ``dt``, ``dl``, ``dr`` as the first six arguments
instead of ``x``, ``y``, ``dx``, ``dy``:

- ``ax.arrow``
- ``ax.quiver``

.. Note::

    In the methods above, by setting the corresponding ``transform``,
    one CAN still pass ``x`` and ``y`` for the plots onto the Cartesian
    coordinates like `data, axes, figure, and display coordinates <https://matplotlib.org/tutorials/advanced/transforms_tutorial.html#sphx-glr-tutorials-advanced-transforms-tutorial-py>`_
    of Matplotlib ``Axes``.

.. Matplotlib

Furthermore, the following methods and attributes are implemented,
which should work as expected from the correspondences of Matplotlib:

- Similarly to ``ax.get_xlabel`` and ``ax.get_ylabel``:
    - ``ax.get_tlabel``
    - ``ax.get_llabel``
    - ``ax.get_rlabel``
- Similarly to ``ax.set_xlabel`` and ``ax.set_ylabel``:
    - ``ax.set_tlabel``
    - ``ax.set_llabel``
    - ``ax.set_rlabel``
- Similarly to ``ax.axhline`` and ``ax.axvline``:
    - ``ax.axtline``
    - ``ax.axlline``
    - ``ax.axrline``
- Similarly to ``ax.axhspan`` and ``ax.axvshan``:
    - ``ax.axtspan``
    - ``ax.axlspan``
    - ``ax.axrspan``
- Similarly to ``ax.xaxis`` and ``ax.yaxis``:
    - ``ax.taxis``
    - ``ax.laxis``
    - ``ax.raxis``

.. Note::

    All the above methods and attributes are designed to be accessible
    only via the `object-oriented API of Matplotlib
    <https://matplotlib.org/api/index.html#the-object-oriented-api>`_.
    The pyplot API may not work as expected.
