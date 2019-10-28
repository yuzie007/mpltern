import numpy as np

import itertools


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
    s = (t + l + r)
    t /= s
    l /= s
    r /= s
    return t, l, r


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
    t, l, r = get_triangular_grid(n, prec)
    # The following works even when y == 0.
    v = -1.0 * (np.log(t ** t) + np.log(l ** l) + np.log(r ** r))
    return t, l, r, v
