"""Tests for datasets"""
import os

import numpy as np
import pytest
from mpltern.datasets import get_dirichlet_pdfs

alphas = ((1.5, 1.5, 1.5), (5.0, 5.0, 5.0), (1.0, 2.0, 2.0), (2.0, 4.0, 8.0))


@pytest.mark.parametrize("alpha", alphas)
def test_get_dirichlet_pdfs(alpha):
    """Test if the PDFs of Dirichlet distributions are calculated correctly."""
    fname = f"Dirichlet_PDF_{alpha[0]:.1f}_{alpha[1]:.1f}_{alpha[2]:.1f}.txt"
    fname = os.path.join(os.path.dirname(__file__), fname)

    tn0_ref, tn1_ref, tn2_ref, pdfs_ref = np.loadtxt(fname, unpack=True)
    tn0, tn1, tn2, pdfs = get_dirichlet_pdfs(n=7, alpha=alpha)

    np.testing.assert_allclose(tn0, tn0_ref)
    np.testing.assert_allclose(tn1, tn1_ref)
    np.testing.assert_allclose(tn2, tn2_ref)
    np.testing.assert_allclose(pdfs, pdfs_ref)
