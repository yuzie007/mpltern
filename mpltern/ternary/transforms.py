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

    def transform_non_affine(self, values):
        """Transform ternary-axis to Cartesian coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            ``s, p == values[:, 0], values[:, 1]``
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
        s = values[:, 0]
        p = values[:, 1]
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

    def transform_non_affine(self, values):
        c0 = self.corners[(self.index + 0) % 3]
        c1 = self.corners[(self.index + 1) % 3]
        c2 = self.corners[(self.index + 2) % 3]
        vectors = np.column_stack((c1 - c0, c2 - c0))
        relative_points = values - c0
        tmp = np.linalg.inv(vectors) @ relative_points.T
        s = 1.0 - (tmp[0] + tmp[1])
        p = tmp[0] / (1.0 - s)
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


class PSTransform(Transform):
    """Transform to place axis-label at side.

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

    def transform_non_affine(self, values):
        """Transform axis-label to Cartesian (likely `display`) coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            ``s, p == values[:, 0], values[:, 1]``
            ``s`` : coordinate along the the edge opposite to the vertex.
            ``s == 0.5`` corresponds to the center position.
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
        return c1 + np.dot(v, values.T).T

    def inverted(self):
        return InvertedPSTransform(
            self.trans, self.corners, self.index)


class InvertedPSTransform(Transform):
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, trans, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans
        self.corners = np.asarray(corners, float)
        self.index = index

    def transform_non_affine(self, values):
        corners = self.trans.transform(self.corners)
        c0 = corners[(self.index + 0) % 3]
        c1 = corners[(self.index + 1) % 3]
        c2 = corners[(self.index + 2) % 3]
        v10 = c0 - c1
        v12 = c2 - c1
        vp = v10 - np.dot(v10, v12) / np.dot(v12, v12) * v12
        vp /= np.linalg.norm(vp)
        v = np.column_stack((v12, vp))
        d = values - c1
        tmp = np.dot(np.linalg.inv(v), d.T).T
        return tmp

    def inverted(self):
        return PSTransform(
            self.trans, self.corners, self.index)


class PCTransform(Transform):
    """Transform to place axis-label at corner.

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

    def transform_non_affine(self, values):
        """Transform axis-label to Cartesian (likely `display`) coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            ``s, p == values[:, 0], values[:, 1]``
            ``s`` : coordinate along the the edge opposite to the vertex.
            ``s == 0.5`` corresponds to the corner position.
            ``p`` : Vertical shift from the first axis in the `display`
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
        v01 = c1 - c0
        v21 = c1 - c2
        # Obtain the vector perpendicular to v21 in the Gram-Schmidt method.
        # The obtained `vp` points inside of the triangle, regardless if the
        # triangle is defined in a clockwise or in a counterclockwise manner.
        vp = v01 - np.dot(v01, v21) / np.dot(v21, v21) * v21
        vp /= np.linalg.norm(vp)
        v = np.column_stack((v21, vp))
        return (c0 - 0.5 * v21) + np.dot(v, values.T).T

    def inverted(self):
        return InvertedPerpendicularCTransform(
            self.trans, self.corners, self.index)


class InvertedPerpendicularCTransform(Transform):
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, trans, corners, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans
        self.corners = np.asarray(corners, float)
        self.index = index

    def transform_non_affine(self, values):
        corners = self.trans.transform(self.corners)
        c0 = corners[(self.index + 0) % 3]
        c1 = corners[(self.index + 1) % 3]
        c2 = corners[(self.index + 2) % 3]
        v01 = c1 - c0
        v21 = c1 - c2
        vp = v01 - np.dot(v01, v21) / np.dot(v21, v21) * v21
        vp /= np.linalg.norm(vp)
        v = np.column_stack((v21, vp))
        d = values - (c0 - 0.5 * v21)
        tmp = np.dot(np.linalg.inv(v), d.T).T
        return tmp

    def inverted(self):
        return PCTransform(
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

    def transform_non_affine(self, values):
        """Transform ternary-axis to Cartesian coordinates

        Parameters
        ----------
        values : (N, 3) array_like
            Points in the barycentric coordinates.

        Returns
        -------
        (x, y) : Cartesian coordinates
        """
        values = np.asarray(values, float)
        values /= np.sum(values, axis=1)[:, np.newaxis]
        return np.dot(values, self.corners)

    def inverted(self):
        return InvertedBarycentricTransform(self.corners)


class InvertedBarycentricTransform(Transform):
    input_dims = 2
    output_dims = 3
    has_inverse = True

    def __init__(self, corners, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners, float)

    def transform_non_affine(self, values):
        xys = np.column_stack((values, np.ones(values.shape[0])))
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
