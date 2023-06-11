###########
Basic Usage
###########

Import mpltern together with Matplotlib as:

.. plot::

    import matplotlib.pyplot as plt
    import mpltern

With this, the projection ``"ternary"`` is registered.
Then, make `TernaryAxes`;

.. plot::

    ax = plt.subplot(projection="ternary")

You can use another normalization constant e.g. 100 using `ternary_sum`.
Ternary-axis labels can be given using e.g. `ax.set_tlabel`.
You can also add grids with `ax.grid`.

.. plot::

    ax = plt.subplot(projection="ternary", ternary_sum=100.0)

    ax.set_tlabel("Top (%)")
    ax.set_llabel("Left (%)")
    ax.set_rlabel("Right (%)")

    ax.grid()

    plt.show()

You can make ternary plots using methods similar to Matplotlib.
You can e.g. use `ax.plot`;
the only difference from Matplotlib is that you give three variables i.e.
`t` (top), `l` (left), `r` (right) instead of `x` and `y`.

.. plot::

    from mpltern.datasets import get_spiral

    ax = plt.subplot(projection="ternary")

    t, l, r = get_spiral()
    # t: [0.33333333 0.33357906 0.33430414 ...]
    # l: [0.33333333 0.33455407 0.33543547 ...]
    # r: [0.33333333 0.33186687 0.33026039 ...]
    ax.plot(t, l, r)

    plt.show()

You can also make filled contour plots using `ax.tricontourf`.

.. plot::

    from mpltern.datasets import get_shanon_entropies

    ax = plt.subplot(projection="ternary")

    t, l, r, entropies = get_shanon_entropies()
    # t: [ 0. 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.1 0.1 0.1 ...]
    # l: [ 0. 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.  0.  0.1 0.2 ...]
    # r: [ 1. 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1 0.  0.9 0.8 0.7 ...]
    # v: [-0. 0.32508297  0.50040242  ...]
    ax.tricontourf(t, l, r, entropies)

    plt.show()

There are more plotting methods and controls.
:doc:`See examples <gallery/index>`.
