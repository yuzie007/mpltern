import os

import numpy as np
import pytest
from mpltern.datasets import get_dirichlet_pdfs

alphas = ((1.5, 1.5, 1.5), (5.0, 5.0, 5.0), (1.0, 2.0, 2.0), (2.0, 4.0, 8.0))


@pytest.mark.parametrize("alpha", alphas)
def test_get_dirichlet_pdfs(alpha):
    fname = f"Dirichlet_PDF_{alpha[0]:.1f}_{alpha[1]:.1f}_{alpha[2]:.1f}.txt"
    fname = os.path.join(os.path.dirname(__file__), fname)
    print(fname)
    t_ref, l_ref, r_ref, v_ref = np.loadtxt(fname, unpack=True)
    t, l, r, v = get_dirichlet_pdfs(n=7, alpha=alpha)
    np.testing.assert_allclose(t, t_ref)
    np.testing.assert_allclose(l, l_ref)
    np.testing.assert_allclose(r, r_ref)
    np.testing.assert_allclose(v, v_ref)
