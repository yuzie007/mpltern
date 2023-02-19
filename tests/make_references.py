import numpy as np
from mpltern.datasets import get_triangular_grid
from scipy.stats import dirichlet

alphas = ((1.5, 1.5, 1.5), (5.0, 5.0, 5.0), (1.0, 2.0, 2.0), (2.0, 4.0, 8.0))
t, l, r = get_triangular_grid(n=7)
x = np.stack((t, l, r), axis=-1)
for alpha in alphas:
    v = dirichlet.pdf(x.T, alpha).T
    print(v)
    fname = f"Dirichlet_PDF_{alpha[0]:.1f}_{alpha[1]:.1f}_{alpha[2]:.1f}.txt"
    np.savetxt(fname, np.stack((t, l, r, v), axis=-1), fmt="%16.9f")
