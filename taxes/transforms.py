import numpy as np

from matplotlib.transforms import Transform


class BAxisTransform(Transform):
    """Transform convenient for BAxis.

    Input
    -----
    0 <= x <= 1, 0 <= y <= 1.
    x == 0 corresponds to bmin.
    x == 1 corresponds to bmax.
    Output
    ------
    (x, y) in the "original" Axes coordinates
    """
    input_dims = 2
    output_dims = 2

    def transform_non_affine(self, points):
        s = points[:, 0]
        p = points[:, 1]
        x = 1.0 - (1.0 - s) * (1.0 - p) - 0.5 * (1.0 - s) * p
        y = (1.0 - s) * p
        return np.column_stack((x, y)).astype(float)


class RAxisTransform(Transform):
    """Transform convenient for RAxis.

    Input
    -----
    0 <= x <= 1, 0 <= y <= 1.
    x == 0 corresponds to rmin.
    x == 1 corresponds to rmax.
    Output
    ------
    (x, y) in the "original" Axes coordinates
    """
    input_dims = 2
    output_dims = 2

    def transform_non_affine(self, points):
        s = points[:, 0]
        p = points[:, 1]
        x = 0.5 + 0.5 * (1.0 - s) * (1.0 - p) - 0.5 * (1.0 - s) * p
        y = s
        return np.column_stack((x, y)).astype(float)


class LAxisTransform(Transform):
    """Transform convenient for LAxis.

    Input
    -----
    0 <= x <= 1, 0 <= y <= 1.
    x == 0 corresponds to lmin.
    x == 1 corresponds to lmax.
    Output
    ------
    (x, y) in the "original" Axes coordinates
    """
    input_dims = 2
    output_dims = 2

    def transform_non_affine(self, points):
        s = points[:, 0]
        p = points[:, 1]
        x = 0.5 * (1.0 - s) * (1.0 - p) + (1.0 - s) * p
        y = 1.0 * (1.0 - s) * (1.0 - p)
        return np.column_stack((x, y)).astype(float)
