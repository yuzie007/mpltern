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

    def __init__(self, corners, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = corners


class BAxisTransform(TernaryTransform):
    def transform_non_affine(self, points):
        corners = self.corners
        s = points[:, 0]
        p = points[:, 1]
        c = corners[0]
        v0 = (corners[1][0] - corners[0][0], corners[1][1] - corners[0][1])
        v1 = (corners[2][0] - corners[0][0], corners[2][1] - corners[0][1])
        x = c[0] + s * v0[0] + (1.0 - s) * p * v1[0]
        y = c[1] + s * v0[1] + (1.0 - s) * p * v1[1]
        return np.column_stack((x, y)).astype(float)


class RAxisTransform(TernaryTransform):
    def transform_non_affine(self, points):
        corners = self.corners
        s = points[:, 0]
        p = points[:, 1]
        c = corners[1]
        v0 = (corners[2][0] - corners[1][0], corners[2][1] - corners[1][1])
        v1 = (corners[0][0] - corners[1][0], corners[0][1] - corners[1][1])
        x = c[0] + s * v0[0] + (1.0 - s) * p * v1[0]
        y = c[1] + s * v0[1] + (1.0 - s) * p * v1[1]
        return np.column_stack((x, y)).astype(float)


class LAxisTransform(TernaryTransform):
    def transform_non_affine(self, points):
        corners = self.corners
        s = points[:, 0]
        p = points[:, 1]
        c = corners[2]
        v0 = (corners[0][0] - corners[2][0], corners[0][1] - corners[2][1])
        v1 = (corners[1][0] - corners[2][0], corners[1][1] - corners[2][1])
        x = c[0] + s * v0[0] + (1.0 - s) * p * v1[0]
        y = c[1] + s * v0[1] + (1.0 - s) * p * v1[1]
        return np.column_stack((x, y)).astype(float)

