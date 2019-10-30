import numpy as np

from matplotlib.transforms import Transform, ScaledTranslation


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
        self.corners = np.asarray(corners, float)
        self.index = index

    def transform_non_affine(self, points):
        c0 = self.corners[(self.index + 0) % 3]
        c1 = self.corners[(self.index + 1) % 3]
        c2 = self.corners[(self.index + 2) % 3]
        s = points[:, 0]
        p = points[:, 1]
        v1 = c1 - c0
        v2 = c2 - c0
        x = c0[0] + (1.0 - s) * (p * v1[0] + (1.0 - p) * v2[0])
        y = c0[1] + (1.0 - s) * (p * v1[1] + (1.0 - p) * v2[1])
        return np.column_stack((x, y)).astype(float)

    def inverted(self):
        return InvertedTernaryTransform(self.corners, self.index)


class InvertedTernaryTransform(Transform):
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners, float)
        self.index = index

    def transform_non_affine(self, points):
        c0 = self.corners[(self.index + 0) % 3]
        c1 = self.corners[(self.index + 1) % 3]
        c2 = self.corners[(self.index + 2) % 3]
        v = np.column_stack((c1 - c0, c2 - c0))
        d = points - c0
        tmp = np.dot(np.linalg.inv(v), d.T)
        s = tmp[0]
        p = tmp[1] / (1.0 - s)
        return np.column_stack((s, p)).astype(float)

    def inverted(self):
        return TernaryTransform(self.corners, self.index)


class _TernaryShiftBase(Transform):
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, indices, figure, axes, pad_points):
        super().__init__()
        self.indices = indices
        self.figure = figure
        self.axes = axes
        self.pad_points = pad_points

    def _get_translation(self):
        corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
        points = self.axes.transTernaryAxes.transform(corners)[self.indices]
        d1 = points[1] - points[0]  # outward against the triangle
        return d1 / np.linalg.norm(d1) * self.pad_points / 72.0


class TernaryShift(_TernaryShiftBase):
    """Shift of tick labels from tick points

    This is essentially a wrapper of ScaledTranslation, but the direction to
    pad it determined on the fly when drawing.
    """
    def transform_non_affine(self, values):
        x, y = self._get_translation()
        trans = ScaledTranslation(x, y, self.figure.dpi_scale_trans)
        return trans.transform(values)

    def inverted(self):
        return InvertedTernaryShift(
            self.indices, self.figure, self.axes, self.pad_points)


class InvertedTernaryShift(_TernaryShiftBase):
    def transform_non_affine(self, values):
        x, y = self._get_translation()
        trans = ScaledTranslation(-x, -y, self.figure.dpi_scale_trans)
        return trans.transform(values)

    def inverted(self):
        return TernaryShift(
            self.indices, self.figure, self.axes, self.pad_points)


class TernaryPerpendicularTransform(Transform):
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
    Coordinates in pixels.
    """
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, trans, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans
        self.corners = np.asarray(corners, float)
        self.index = index

    def transform_non_affine(self, points):
        corners = self.trans.transform(self.corners)
        c0 = corners[(self.index + 0) % 3]
        c1 = corners[(self.index + 1) % 3]
        c2 = corners[(self.index + 2) % 3]
        v10 = c0 - c1
        v12 = c2 - c1
        # Obtain the vector perpendicular to v12 in the Gram-Schmidt method.
        # The obtained `vp` points inside of the triangle, regardless if the
        # triangle is defined in a clockwise or in a counterclockwise manner.
        vp = v10 - np.dot(v10, v12) / np.dot(v12, v12) * v12
        vp /= np.linalg.norm(vp)
        v = np.column_stack((v12, vp))
        return c1 + np.dot(v, points.T).T

    def inverted(self):
        return InvertedTernaryPerpendicularTransform(
            self.trans, self.corners, self.index)


class InvertedTernaryPerpendicularTransform(Transform):
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, trans, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans
        self.corners = np.asarray(corners, float)
        self.index = index

    def transform_non_affine(self, points):
        corners = self.trans.transform(self.corners)
        c0 = corners[(self.index + 0) % 3]
        c1 = corners[(self.index + 1) % 3]
        c2 = corners[(self.index + 2) % 3]
        v10 = c0 - c1
        v12 = c2 - c1
        vp = v10 - np.dot(v10, v12) / np.dot(v12, v12) * v12
        vp /= np.linalg.norm(vp)
        v = np.column_stack((v12, vp))
        d = points - c1
        tmp = np.dot(np.linalg.inv(v), d.T).T
        return tmp

    def inverted(self):
        return TernaryPerpendicularTransform(
            self.trans, self.corners, self.index)


class BarycentricTransform(Transform):
    """
    This transforms the points in the barycentric coordinates to the original
    ones. If `corners` are in the `Axes` coordinates, this returns the points
    in the `Axes` coordinates.
    """
    input_dims = 3
    output_dims = 2
    has_inverse = True

    def __init__(self, corners, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners, float)

    def transform_non_affine(self, points):
        points = np.asarray(points, float)
        points /= np.sum(points, axis=1)[:, np.newaxis]
        return np.dot(points, self.corners)

    def inverted(self):
        return InvertedBarycentricTransform(self.corners)


class InvertedBarycentricTransform(Transform):
    input_dims = 2
    output_dims = 3
    has_inverse = True

    def __init__(self, corners, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners, float)

    def transform_non_affine(self, points):
        xys = np.column_stack((points, np.ones(points.shape[0])))
        v = np.column_stack((self.corners, np.ones(3)))
        return np.dot(xys, np.linalg.inv(v))

    def inverted(self):
        return BarycentricTransform(self.corners)


class TernaryScaleTransform(Transform):
    """
    viewTernaryScale : Bbox
    """
    input_dims = 3
    output_dims = 3
    has_inverse = True

    def __init__(self, ternary_scale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_scale = ternary_scale

    def transform_non_affine(self, values):
        return np.asarray(values, float) / self.ternary_scale

    def inverted(self):
        return InvertedTernaryScaleTransform(self.ternary_scale)


class InvertedTernaryScaleTransform(Transform):
    input_dims = 3
    output_dims = 3
    has_inverse = True

    def __init__(self, ternary_scale, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_scale = ternary_scale

    def transform_non_affine(self, values):
        return np.asarray(values, float) * self.ternary_scale

    def inverted(self):
        return TernaryScaleTransform(self.ternary_scale)
