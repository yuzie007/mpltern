import numpy as np

import matplotlib.pyplot as plt
from matplotlib.testing.decorators import image_comparison
import mpltern  # noqa: F401


@image_comparison(
    baseline_images=["base"],
    extensions=["pdf"],
    tol=0.1,
    style="mpl20",
)
def test_base():
    np.random.seed(19680801)
    t, l, r = np.random.dirichlet(alpha=(2.0, 4.0, 8.0), size=100000).T
    ax = plt.subplot(projection="ternary")
    # If "face" (default), small hexagons look overlapping with each other.
    ax.hexbin(t, l, r, edgecolors="none")


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
    ax.hexbin(t, l, r, edgecolors="none")
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
    ax.hexbin(t, l, r, gridsize=40, extent=extent, edgecolors="none")


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
    ax.hexbin(t, l, r, edgecolors="none")
