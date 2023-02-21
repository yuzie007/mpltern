import os

import numpy as np
from mpltern import tribin_helpers


def test_calc_serial_index_of_hexagons():
    fname = f"tribin_indices.txt"
    fname = os.path.join(os.path.dirname(__file__), fname)
    g, it, il, ir, i_ref = np.loadtxt(fname, dtype=int, unpack=True)
    i = tribin_helpers.ternary_to_serial(g, it, il, ir)
    np.testing.assert_array_equal(i, i_ref)


def test_calc_ternary_index_of_hexagons():
    fname = f"tribin_indices.txt"
    fname = os.path.join(os.path.dirname(__file__), fname)
    g, it_ref, il_ref, ir_ref, i = np.loadtxt(fname, dtype=int, unpack=True)
    it, il, ir = tribin_helpers.serial_to_ternary(g, i)
    np.testing.assert_array_equal(it, it_ref)
    np.testing.assert_array_equal(il, il_ref)
    np.testing.assert_array_equal(ir, ir_ref)
