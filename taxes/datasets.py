import numpy as np

import itertools
from scipy.special import xlogy


def get_spiral(ternary_scale=1.0):
    """Archimedean spiral in ternary coordinates

    https://en.wikipedia.org/wiki/Archimedean_spiral
    """
    t = np.linspace(0, np.pi * 10, 201)
    a = 0.01
    b = 1.0 / 3.0 + a * t * np.sin(t + np.pi / 3.0 * 0.0)
    r = 1.0 / 3.0 + a * t * np.sin(t + np.pi / 3.0 * 2.0)
    l = 1.0 / 3.0 + a * t * np.sin(t + np.pi / 3.0 * 4.0)
    return b * ternary_scale, r * ternary_scale, l * ternary_scale


def get_scatter_points(n=201, seed=19680801):
    np.random.seed(seed)
    b = np.random.rand(n)
    r = np.random.rand(n)
    l = np.random.rand(n)
    s = (b + r + l)
    b /= s
    r /= s
    l /= s
    return b, r, l


def get_triangular_grid(n=11, prec=1e-6):
    t = np.linspace(0, 1, n)
    ps = []
    for tmp in itertools.product(t, repeat=3):
        if abs(sum(tmp) - 1.0) > prec:
            continue
        ps.append(tmp)
    ps = np.asarray(ps)
    return ps[:, 0], ps[:, 1], ps[:, 2]


def get_shanon_entropies(n=11, prec=1e-6):
    b, r, l = get_triangular_grid(n, prec)
    # The following works even e.g. p0 == 0.
    v = -1.0 * (xlogy(b, b) + xlogy(r, r) + xlogy(l, l))
    return b, r, l, v
