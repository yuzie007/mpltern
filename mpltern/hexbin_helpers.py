import numpy as np
from typing import Tuple


def calc_serial_index_of_hexagons(g: int, it: int, il: int, ir: int) -> int:
    """Calculate serial index of hexagons from ternary indices.

    Parameters
    ----------
    g : int
        Grid size.
    it : int
        Index for the t axis.
    il : int
        Index for the l axis.
    ir : int
        Index for the r axis.

    Returns
    -------
    i : int
        Serial index of hexagons from ``0`` to ``(g + 1) * (g + 1) // 2``.
        If (``it``, ``il``, ``ir``) is out of the triangle with the grid size,
        ``i == -1``.

    Examples
    --------
    The following gives the correspondence between the ternary and the serial
    indices when ``g == 3``.
    +------------------+-------+
    | ``(it, il, ir)`` | ``i`` |
    +==================+=======+
    | ``(3, 0, 0)``    | ``0`` |
    | ``(2, 1, 0)``    | ``1`` |
    | ``(2, 0, 1)``    | ``2`` |
    | ``(1, 2, 0)``    | ``3`` |
    | ``(1, 1, 1)``    | ``4`` |
    | ``(1, 0, 2)``    | ``5`` |
    | ``(0, 3, 0)``    | ``6`` |
    | ``(0, 2, 1)``    | ``7`` |
    | ``(0, 1, 2)``    | ``8`` |
    | ``(0, 0, 3)``    | ``9`` |
    +------------------+-------+
    """
    tmpt = (0 <= it) & (it <= g)
    tmpl = (0 <= il) & (il <= g)
    tmpr = (0 <= ir) & (ir <= g)
    is_inside = tmpt & tmpl & tmpr
    return np.where(is_inside, (g - it) * (g - it + 1) // 2 + ir, -1)


def calc_ternary_indices_of_hexagons(g: int, i: int) -> Tuple[int]:
    """Calculate ternary indices of hexagons from serial index.

    Parameters
    ----------
    g : int
        Grid size.
    i : int
        Serial index of hexagons from ``0`` to ``(g + 1) * (g + 2) // 2``.

    Returns
    -------
    (it, il, ir) : Tuple[int]
        Ternary indices of hexagons.

        https://en.wikipedia.org/wiki/Triangular_number#Triangular_roots_and_tests_for_triangular_numbers
    """
    it = g - (np.floor(np.sqrt(8 * i + 1)).astype(int) - 1) // 2
    ir = i - (g - it) * (g - it + 1) // 2
    il = g - (it + ir)
    return it, il, ir
