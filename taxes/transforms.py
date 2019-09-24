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
    has_inverse = True

    def __init__(self, corners, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = corners


class InvertedTernaryTransform(Transform):
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = corners
        self.index = index

    def transform_non_affine(self, points):
        c0 = self.corners[(self.index + 0) % 3]
        c1 = self.corners[(self.index + 1) % 3]
        c2 = self.corners[(self.index + 2) % 3]
        v = [
            [c1[0] - c0[0], c2[0] - c0[0]],
            [c1[1] - c0[1], c2[1] - c0[1]],
        ]
        v = np.array(v)
        d = points - c0
        tmp = np.dot(np.linalg.inv(v), d.T)
        s = tmp[0]
        p = tmp[1] / (1.0 - s)
        return np.column_stack((s, p)).astype(float)


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

    def inverted(self):
        return InvertedTernaryTransform(self.corners, 0)


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

    def inverted(self):
        return InvertedTernaryTransform(self.corners, 1)


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

    def inverted(self):
        return InvertedTernaryTransform(self.corners, 2)
