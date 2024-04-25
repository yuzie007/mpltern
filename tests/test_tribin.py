import numpy as np

import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison, check_figures_equal
from matplotlib.colors import LogNorm
import mpltern  # noqa: F401


@image_comparison(
    baseline_images=["base"],
    extensions=["pdf"],
    style="mpl20",
)
def test_base():
    np.random.seed(19680801)
    t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=100000).T
    ax = plt.subplot(projection="ternary")
    # If "face" (default), small hexagons look overlapping with each other.
    ax.tribin(t, l, r, edgecolors="none")


@check_figures_equal(extensions=('pdf',))
def test_ternary_normalization(fig_test, fig_ref):
    """Test if ternary values are automatically normalized correctly."""
    np.random.seed(19680801)
    size = 1000
    t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=size).T

    ax = fig_ref.add_subplot(projection="ternary")
    ax.tribin(t, l, r, gridsize=10, edgecolors="none")

    scale = np.arange(1, size + 1)
    t *= scale
    l *= scale
    r *= scale

    ax = fig_test.add_subplot(projection="ternary")
    ax.tribin(t, l, r, gridsize=10, edgecolors="none")


@check_figures_equal(extensions=('pdf',))
def test_weights(fig_test, fig_ref):
    """Test if the `C` option works correctly."""
    np.random.seed(19680801)
    size = 1000
    t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=size).T

    ax = fig_test.add_subplot(projection="ternary")
    ax.tribin(t, l, r, C=[1] * size, gridsize=10, reduce_C_function=sum)

    ax = fig_ref.add_subplot(projection="ternary")
    ax.tribin(t, l, r, gridsize=10)


@image_comparison(
    baseline_images=["ternary_lim"],
    extensions=["pdf"],
    style="mpl20",
)
def test_ternary_lim():
    np.random.seed(19680801)
    t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=100000).T
    ax = plt.subplot(projection="ternary")
    # If "face" (default), small hexagons look overlapping with each other.
    ax.tribin(t, l, r, edgecolors="none")
    ax.set_ternary_lim(
        0.1, 0.5,  # tmin, tmax
        0.2, 0.6,  # lmin, lmax
        0.3, 0.7,  # rmin, rmax
    )


@image_comparison(
    baseline_images=["extent"],
    extensions=["pdf"],
    style="mpl20",
)
def test_extent():
    np.random.seed(19680801)
    t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=100000).T
    ax = plt.subplot(projection="ternary")
    extent = (0.1, 0.5, 0.2, 0.6, 0.3, 0.7)
    # If "face" (default), small hexagons look overlapping with each other.
    ax.tribin(t, l, r, gridsize=40, extent=extent, edgecolors="none")


@image_comparison(
    baseline_images=["given_triangles"],
    extensions=["pdf"],
    style="mpl20",
)
def test_given_triangles():
    corners = ((0.5, 0.0), (1.0, 0.5), (0.0, 1.0))
    np.random.seed(19680801)
    t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=100000).T
    ax = plt.subplot(projection="ternary", corners=corners, rotation=0)
    # If "face" (default), small hexagons look overlapping with each other.
    ax.tribin(t, l, r, edgecolors="none")


@check_figures_equal(extensions=('pdf',))
def test_bins_and_norm(fig_test, fig_ref):
    np.random.seed(19680801)
    t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=100000).T

    ax = fig_test.add_subplot(projection="ternary")
    ax.tribin(t, l, r, bins="log")

    ax = fig_ref.add_subplot(projection="ternary")
    ax.tribin(t, l, r, norm=LogNorm())


def test_ndarray_cast():
    """Test if non-float ndarray can be passed without errors.

    https://github.com/yuzie007/mpltern/issues/15
    https://numpy.org/doc/stable/reference/arrays.dtypes.html
    """
    tn0 = np.array((1,), dtype='>u2')
    tn1 = np.array((0,), dtype='>u2')
    tn2 = np.array((0,), dtype='>u2')

    fig = plt.figure()
    ax = fig.add_subplot(projection="ternary")
    ax.tribin(tn0, tn1, tn2, gridsize=10, edgecolors="none")
