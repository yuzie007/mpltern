import os

import numpy as np
from mpltern.hexbin_helpers import (calc_serial_index_of_hexagons,
                                    calc_ternary_indices_of_hexagons)


def test_calc_serial_index_of_hexagons():
    fname = f"hexbin_indices.txt"
    fname = os.path.join(os.path.dirname(__file__), fname)
    g, it, il, ir, i_ref = np.loadtxt(fname, dtype=int, unpack=True)
    i = calc_serial_index_of_hexagons(g, it, il, ir)
    assert np.array_equal(i, i_ref)


def test_calc_ternary_index_of_hexagons():
    fname = f"hexbin_indices.txt"
    fname = os.path.join(os.path.dirname(__file__), fname)
    g, it_ref, il_ref, ir_ref, i = np.loadtxt(fname, dtype=int, unpack=True)
    it, il, ir = calc_ternary_indices_of_hexagons(g, i)
    assert np.array_equal(it, it_ref)
    assert np.array_equal(il, il_ref)
    assert np.array_equal(ir, ir_ref)
