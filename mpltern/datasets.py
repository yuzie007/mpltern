import itertools
from math import gamma

import numpy as np


def get_spiral(ternary_scale=1.0):
    """Archimedean spiral in ternary coordinates

    https://en.wikipedia.org/wiki/Archimedean_spiral
    """
    theta = np.linspace(0, np.pi * 10, 201)
    a = 0.01
    t = 1.0 / 3.0 + a * theta * np.sin(theta + np.pi / 3.0 * 0.0)
    l = 1.0 / 3.0 + a * theta * np.sin(theta + np.pi / 3.0 * 2.0)
    r = 1.0 / 3.0 + a * theta * np.sin(theta + np.pi / 3.0 * 4.0)
    return t * ternary_scale, l * ternary_scale, r * ternary_scale


def get_scatter_points(n=201, seed=19680801):
    np.random.seed(seed)
    t = np.random.rand(n)
    l = np.random.rand(n)
    r = np.random.rand(n)
    s = t + l + r
    t /= s
    l /= s
    r /= s
    return t, l, r


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
    ps = []
    for tmp in itertools.product(t, repeat=3):
        if abs(sum(tmp) - 1.0) > prec:
            continue
        ps.append(tmp)
    ps = np.array(ps)
    return ps[:, 0], ps[:, 1], ps[:, 2]


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
    t, l, r = get_triangular_grid(n, prec)
    # The following works even when y == 0.
    entropies = -1.0 * (np.log(t**t) + np.log(l**l) + np.log(r**r))
    return t, l, r, entropies


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
    t, l, r = get_triangular_grid(n, prec)
    x = np.stack((t, l, r), axis=-1)
    alpha = np.array(alpha)
    c = gamma(np.sum(alpha)) / np.prod([gamma(_) for _ in alpha])
    v = c * np.prod(x ** (alpha - 1.0), axis=1)
    return t, l, r, v
