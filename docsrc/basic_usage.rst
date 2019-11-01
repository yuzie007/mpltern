###########
Basic Usage
###########

To use mpltern functionalities, one first needs to import mpltern as well
as Matplotlib as:

.. code-block:: python

    import matplotlib.pyplot as plt
    import mpltern

By ``import mpltern``, a Matplotlib projection ``'ternary'`` is
registered inside. One can then create ``TernaryAxes`` e.g. as:

.. code-block:: python

    ax = plt.subplot(projection='ternary')

It is already possible to create ternary plots using the methods in ``ax``.
For example:

.. code-block:: python

    from mpltern.ternary.datasets import get_spiral

    t, l, r = mpltern.datasets.get_spiral()
    ax.plot(t, l, r)
    plt.show()

You may see the following Archimedean spiral in the triangle.

.. image:: basic_1.svg

Contour-like plots are also possible in mpltern.

.. code-block:: python

    ax = plt.subplot(projection='ternary')

    from mpltern.ternary.datasets import get_shanon_entropies

    t, l, r, v = get_shanon_entropies()
    ax.tricontourf(t, l, r, v)
    plt.show()

.. image:: basic_2.svg

See also `more examples <gallery/index.html>`_.
