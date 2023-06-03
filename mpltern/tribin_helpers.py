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
    it0 = np.floor(ft).astype(int)
    il0 = np.floor(fl).astype(int)
    ir0 = np.floor(fr).astype(int)

    # Using digitize, values that fall on an edge are put in the right bin.
    # For the rightmost bin, we want values equal to the right edge to be
    # counted in the last bin, and not as an outlier.
    # https://numpy.org/doc/stable/reference/generated/numpy.histogramdd.html
    it = np.where(t == tmax, it0 - 1, it0)
    il = np.where(l == lmax, il0 - 1, il0)
    ir = np.where(r == rmax, ir0 - 1, ir0)

    return st, sl, sr, it, il, ir


def ternary_to_serial(gridsize: int, it: int, il: int, ir: int) -> int:
    """Convert serial index of triangles from ternary indices.

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
        Serial index of triangles from ``0`` to ``gridsize ** 2 - 1``.
        If (``it``, ``il``, ``ir``) is out of the triangle with the grid size,
        ``i == -1``.
        Upward triangles come first, followed by downward triangles.

    Examples
    --------
    The following gives the correspondence between the ternary and the serial
    indices when ``g == 3``.
    +------------------+-------+
    | ``(it, il, ir)`` | ``i`` |
    +==================+=======+
    | ``(2, 0, 0)``    | ``0`` |
    | ``(1, 1, 0)``    | ``1`` |
    | ``(1, 0, 1)``    | ``2`` |
    | ``(0, 2, 0)``    | ``3`` |
    | ``(0, 1, 1)``    | ``4`` |
    | ``(0, 0, 2)``    | ``5`` |
    | ``(1, 0, 0)``    | ``6`` |
    | ``(0, 1, 0)``    | ``7`` |
    | ``(0, 0, 1)``    | ``8`` |
    +------------------+-------+
    """
    tmpt = (0 <= it) & (it <= gridsize)
    tmpl = (0 <= il) & (il <= gridsize)
    tmpr = (0 <= ir) & (ir <= gridsize)
    is_inside = tmpt & tmpl & tmpr
    i0 = (gridsize - it - 1) * (gridsize - it) // 2 + ir
    shift = gridsize * (gridsize + 1) // 2
    i1 = (gridsize - it - 2) * (gridsize - it - 1) // 2 + ir
    i = np.where(it + il + ir + 1 == gridsize, i0, i1 + shift)
    return np.where(is_inside, i, -1)


def serial_to_ternary(gridsize: int, i: int) -> Sequence[int]:
    """Convert ternary indices of triangles to serial index.

    Parameters
    ----------
    gridsize : int
        Grid size.
    i : int
        Serial index of triangles from ``0`` to ``gridsize ** 2 - 1``.

    Returns
    -------
    (it, il, ir) : Tuple[int]
        Ternary indices of triangles.
    """
    upward = (i < gridsize * (gridsize + 1) // 2)

    i0 = np.where(upward, i, 0)

    it0 = (gridsize - 1) - (np.floor(np.sqrt(8 * i0 + 1)).astype(int) - 1) // 2
    ir0 = i0 - (gridsize - it0 - 1) * (gridsize - it0) // 2
    il0 = gridsize - (it0 + ir0 + 1)

    i1 = np.where(upward, 0, i - gridsize * (gridsize + 1) // 2)

    it1 = (gridsize - 2) - (np.floor(np.sqrt(8 * i1 + 1)).astype(int) - 1) // 2
    ir1 = i1 - (gridsize - it1 - 2) * (gridsize - it1 - 1) // 2
    il1 = gridsize - (it1 + ir1 + 2)

    it = np.where(upward, it0, it1)
    il = np.where(upward, il0, il1)
    ir = np.where(upward, ir0, ir1)

    return it, il, ir
