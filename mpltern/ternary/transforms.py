"""
Transforms used for ternary plots.

Notes
-----
Inside ``Transform.transform`` of Matplotlib, the last dimension of the input
values are forced to be the same as ``input_dims``.
"""
import numpy as np

from matplotlib.transforms import Transform, ScaledTranslation


class TernaryTransform(Transform):
    """Transform convenient for ticks in TernaryAxis.

    Parameters
    ----------
    corners : (3, 2) array_like
        Corners of the triangle in Cartesian coordinates.
    index : int
        Index of the axis; t: 0, l: 1, r: 2.
    """
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners, float)
        self.index = index

    def transform_non_affine(self, points):
        """Transform ternary-axis to Cartesian coordinates

        Parameters
        ----------
        points : (N, 2) array_like
            ``s, p == points[:, 0], points[:, 1]``
            ``s`` : ternary coordinate of the given axis.
            ``s == 0`` : ternary min.
            ``s == 1`` : ternary max.
            ``p`` : coordinate ``perpendicular`` to the given axis.
            ``p == 0`` : on the edge for tick1.
            ``p == 1`` : on the edge for tick2.

        Returns
        -------
        (x, y) : Cartesian coordinates
        """
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
    pad is determined on the fly when drawing.
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

    Parameters
    ----------
    trans : ``Transform``
        ``Axes.transAxes`` is supposed to be given.
    corners : (3, 2) array_like
        Corners of the triangle in Cartesian coordinates.
    index : int
        Index of the axis; t: 0, l: 1, r: 2.
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
        """Transform axis-label to Cartesian (likely `display`) coordinates

        Parameters
        ----------
        points : (N, 2) array_like
            ``s, p == points[:, 0], points[:, 1]``
            ``s`` : ternary coordinate of the given axis.
            ``s == 0`` : ternary min.
            ``s == 1`` : ternary max.
            ``p`` : Vertical shift from the ternary axis in the `display`
            coordinate system. ``p > 0`` and ``p < 0`` are towards the inside
            and the outside of the triangle.

        Returns
        -------
        (x, y) : Coordinates in the `display` (pixel) coordinates.
        """
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
    """Transform from the barycentric to Cartesian coordinates.

    https://en.wikipedia.org/wiki/Barycentric_coordinate_system

    Parameters
    ----------
    corners : (3, 2) array_like
        Corners of the triangle in Cartesian coordinates.
        If `corners` are in the `Axes` coordinates, this can be the transform
        for the `Axes` coordinates.
    """
    input_dims = 3
    output_dims = 2
    has_inverse = True

    def __init__(self, corners, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners, float)

    def transform_non_affine(self, points):
        """Transform ternary-axis to Cartesian coordinates

        Parameters
        ----------
        points : (N, 3) array_like
            Points in the barycentric coordinates.

        Returns
        -------
        (x, y) : Cartesian coordinates
        """
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
