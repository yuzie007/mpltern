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
