import numpy as np
from typing import Sequence


def calc_ternary_indices(t, l, r, gridsize: int, extent: Sequence[float]):
    tmin, tmax, lmin, lmax, rmin, rmax = extent

    # side lengths along ternary axes
    st = (tmax - tmin) / gridsize
    sl = (lmax - lmin) / gridsize
    sr = (rmax - rmin) / gridsize

    # ternary coordinates in fraction of (st, sl, sr)
    ft = (t - tmin) / st
    fl = (l - lmin) / sl
    fr = (r - rmin) / sr

    # first rounding
    it0 = np.rint(ft).astype(int)
    il0 = np.rint(fl).astype(int)
    ir0 = np.rint(fr).astype(int)

    # When the point is close to a corner of a hexagon, it0 + il0 + ir0 does
    # not agree with gridsize. In such a case, the ternary coordinate that is
    # the furthest from the first rounded integer should be corrected.
    # https://www.redblobgames.com/grids/hexagons/#rounding
    # https://stackoverflow.com/a/37205672

    # check if the point is close to a corner of a hexagon
    b0 = it0 + il0 + ir0 == gridsize

    # differences from the first rounded values
    dt = ft - it0
    dl = fl - il0
    dr = fr - ir0

    # which axis shows the largest difference from the first rounded value
    i0 = np.stack((abs(dt), abs(dl), abs(dr)), axis=0).argmax(axis=0)

    # last rounding
    it = np.where(b0, it0, np.where(i0 == 0, gridsize - (il0 + ir0), it0))
    il = np.where(b0, il0, np.where(i0 == 1, gridsize - (ir0 + it0), il0))
    ir = np.where(b0, ir0, np.where(i0 == 2, gridsize - (it0 + il0), ir0))

    return st, sl, sr, it, il, ir


def ternary_to_serial(gridsize: int, it: int, il: int, ir: int) -> int:
    """Convert serial index of hexagons from ternary indices.

    Parameters
    ----------
    gridsize : int
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
        Serial index of hexagons from ``0`` to ``(g + 1) * (g + 2) // 2 - 1``.
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
    tmpt = (0 <= it) & (it <= gridsize)
    tmpl = (0 <= il) & (il <= gridsize)
    tmpr = (0 <= ir) & (ir <= gridsize)
    is_inside = tmpt & tmpl & tmpr
    i = (gridsize - it) * (gridsize - it + 1) // 2 + ir
    return np.where(is_inside, i, -1)


def serial_to_ternary(gridsize: int, i: int) -> Sequence[int]:
    """Convert ternary indices of hexagons to serial index.

    Parameters
    ----------
    gridsize : int
        Grid size.
    i : int
        Serial index of hexagons from ``0`` to ``(g + 1) * (g + 2) // 2 - 1``.

    Returns
    -------
    (it, il, ir) : Tuple[int]
        Ternary indices of hexagons.

        https://en.wikipedia.org/wiki/Triangular_number#Triangular_roots_and_tests_for_triangular_numbers
    """
    it = gridsize - (np.floor(np.sqrt(8 * i + 1)).astype(int) - 1) // 2
    ir = i - (gridsize - it) * (gridsize - it + 1) // 2
    il = gridsize - (it + ir)
    return it, il, ir
