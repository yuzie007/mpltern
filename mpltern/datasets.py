import itertools
from math import gamma

import numpy as np


def get_spiral(constant=1.0):
    """Archimedean spiral in ternary coordinates

    https://en.wikipedia.org/wiki/Archimedean_spiral
    """
    theta = np.linspace(0, np.pi * 10, 201)
    amp = 0.01
    tn0 = 1.0 / 3.0 + amp * theta * np.sin(theta + np.pi / 3.0 * 0.0)
    tn1 = 1.0 / 3.0 + amp * theta * np.sin(theta + np.pi / 3.0 * 2.0)
    tn2 = 1.0 / 3.0 + amp * theta * np.sin(theta + np.pi / 3.0 * 4.0)
    return tn0 * constant, tn1 * constant, tn2 * constant


def get_scatter_points(n=201, seed=19680801):
    np.random.seed(seed)
    tn0 = np.random.rand(n)
    tn1 = np.random.rand(n)
    tn2 = np.random.rand(n)
    constant = tn0 + tn1 + tn2
    tn0 /= constant
    tn1 /= constant
    tn2 /= constant
    return tn0, tn1, tn2


def get_triangular_grid(n=11, prec=1e-6):
    """Triangular grid

    Parameters
    ----------
    n : int, optional
        Number of grid points along one ternary axis, by default 11
    prec : float, optional
        Tolerance for triangular points, by default 1e-6

    Returns
    -------
    (t, l, r) : tuple[np.ndarray]
        Ternary coordinates.
    """
    # top axis in descending order to start from the top point
    t = np.linspace(1, 0, n)
    points = []
    for tmp in itertools.product(t, repeat=3):
        if abs(sum(tmp) - 1.0) > prec:
            continue
        points.append(tmp)
    points = np.array(points)
    return points[:, 0], points[:, 1], points[:, 2]


def get_shanon_entropies(n=61, prec=1e-6):
    """Shanon entropy

    https://en.wikipedia.org/wiki/Entropy_(information_theory)

    Parameters
    ----------
    n : int
        Number of points for each coordinate, by default 61
    prec : float
        Tolerance for triangular points, by default 1e-6
    """
    tn0, tn1, tn2 = get_triangular_grid(n, prec)
    # The following works even when y == 0.
    entropies = -1.0 * (np.log(tn0**tn0) + np.log(tn1**tn1) + np.log(tn2**tn2))
    return tn0, tn1, tn2, entropies


def get_dirichlet_pdfs(n=61, alpha=(1.0, 1.0, 1.0), prec=1e-6):
    """Probability density function of the Dirichlet distribution

    https://en.wikipedia.org/wiki/Dirichlet_distribution

    Parameters
    ----------
    n : int
        Number of points for each coordinate, by default 61
    alpha : by default (1.0, 1.0, 1.0)
    prec : float
        Tolerance for triangular points, by default 1e-6
    """
    tn0, tn1, tn2 = get_triangular_grid(n, prec)
    x = np.stack((tn0, tn1, tn2), axis=-1)
    alpha = np.array(alpha)
    c = gamma(np.sum(alpha)) / np.prod([gamma(_) for _ in alpha])
    pdfs = c * np.prod(x ** (alpha - 1.0), axis=1)
    return tn0, tn1, tn2, pdfs
