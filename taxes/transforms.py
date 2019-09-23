import numpy as np

from matplotlib.transforms import Transform


class TernaryTransform(Transform):
    """Transform convenient for TernaryAxis.

    Input
    -----
    0 <= x <= 1, 0 <= y <= 1.
    x == 0 corresponds to ternary min.
    x == 1 corresponds to ternary max.
    Output
    ------
    (x, y) in the "original" Axes coordinates
    """
    input_dims = 2
    output_dims = 2


class BAxisTransform(TernaryTransform):
    def transform_non_affine(self, points):
        s = points[:, 0]
        p = points[:, 1]
        x = 1.0 - (1.0 - s) * (1.0 - p) - 0.5 * (1.0 - s) * p
        y = (1.0 - s) * p
        return np.column_stack((x, y)).astype(float)


class RAxisTransform(TernaryTransform):
    def transform_non_affine(self, points):
        s = points[:, 0]
        p = points[:, 1]
        x = 0.5 + 0.5 * (1.0 - s) * (1.0 - p) - 0.5 * (1.0 - s) * p
        y = s
        return np.column_stack((x, y)).astype(float)


class LAxisTransform(TernaryTransform):
    def transform_non_affine(self, points):
        s = points[:, 0]
        p = points[:, 1]
        x = 0.5 * (1.0 - s) * (1.0 - p) + (1.0 - s) * p
        y = 1.0 * (1.0 - s) * (1.0 - p)
        return np.column_stack((x, y)).astype(float)

