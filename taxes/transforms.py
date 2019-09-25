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

    def __init__(self, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners)
        self.index = index

    def transform_non_affine(self, points):
        c0 = self.corners[(self.index + 0) % 3]
        c1 = self.corners[(self.index + 1) % 3]
        c2 = self.corners[(self.index + 2) % 3]
        s = points[:, 0]
        p = points[:, 1]
        v0 = (c1[0] - c0[0], c1[1] - c0[1])
        v1 = (c2[0] - c0[0], c2[1] - c0[1])
        x = c0[0] + s * v0[0] + (1.0 - s) * p * v1[0]
        y = c0[1] + s * v0[1] + (1.0 - s) * p * v1[1]
        return np.column_stack((x, y)).astype(float)

    def inverted(self):
        return InvertedTernaryTransform(self.corners, self.index)


class InvertedTernaryTransform(Transform):
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners)
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

    def inverted(self):
        return TernaryTransform(self.corners, self.index)


class VerticalTernaryTransform(Transform):
    """Transform convenient for axis-labels in TernaryAxis.

    Input
    -----
    0 <= x <= 1
    x == 0 corresponds to ternary min.
    x == 1 corresponds to ternary max.

    y : float
        Vertical shift from the ternary axis in the `display`
        coordinate system.

    Output
    ------
    """
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, trans, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans
        self.corners = np.asarray(corners)
        self.index = index

    def transform_non_affine(self, points):
        corners = self.trans.transform(self.corners)
        c0 = corners[(self.index + 0) % 3]
        c1 = corners[(self.index + 1) % 3]
        v0 = c1 - c0
        v1 = [-v0[1], v0[0]]  # Vertical
        v1 /= np.linalg.norm(v1)
        v = np.column_stack((v0, v1))
        return c0 + np.dot(v, points.T).T

    def inverted(self):
        return InvertedVerticalTernaryTransform(self.trans, self.corners, self.index)


class InvertedVerticalTernaryTransform(Transform):
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, trans, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans
        self.corners = np.asarray(corners)
        self.index = index

    def transform_non_affine(self, points):
        corners = self.trans.transform(self.corners)
        c0 = corners[(self.index + 0) % 3]
        c1 = corners[(self.index + 1) % 3]
        v0 = c1 - c0
        v1 = [-v0[1], v0[0]]
        v1 /= np.linalg.norm(v1)
        v = np.column_stack((v0, v1))
        d = points - c0
        tmp = np.dot(np.linalg.inv(v), d.T).T
        return tmp

    def inverted(self):
        return VerticalTernaryTransform(self.corners, self.index)


class TernaryDataTransform(Transform):
    input_dims = 3
    output_dims = 2
    has_inverse = True

    def __init__(self, transLimits, scale, corners, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transLimits = transLimits
        self.scale = scale
        self.corners = np.asarray(corners)

    def transform_non_affine(self, points):
        tmp = np.roll(self.corners, shift=-1, axis=0)
        tmp = np.dot(points, tmp) / self.scale
        return self.transLimits.inverted().transform(tmp)

    def inverted(self):
        return InvertedTernaryDataTransform(self.corners)


class InvertedTernaryDataTransform(Transform):
    input_dims = 2
    output_dims = 3
    has_inverse = True

    def __init__(self, corners, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners)

    def transform_non_affine(self, points):
        raise NotImplementedError

    def inverted(self):
        return TernaryDataTransform(self.corners)
