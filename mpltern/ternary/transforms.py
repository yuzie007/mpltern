"""
Transforms used for ternary plots.

Notes
-----
Inside ``Transform.transform`` of Matplotlib, the last dimension of the input
values are forced to be the same as ``input_dims``.
"""
import numpy as np

from matplotlib.transforms import Affine2DBase, Transform, ScaledTranslation


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

    def inverted(self):
        raise NotImplementedError


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


class PSTransform(Affine2DBase):
    """Transform to place axis-label at side.

    Parameters
    ----------
    trans : ``Transform``
        Transform derived from ``TernaryTransform`` is supposed to be given.
    """
    input_dims = 2
    output_dims = 2

    def __init__(self, trans: Transform, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans

    def get_matrix(self):
        """Transform axis-label to Cartesian (likely `display`) coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            ``s, p == values[:, 0], values[:, 1]``
            ``s`` : coordinate along the the edge opposite to the vertex.
            ``s == 0.5`` corresponds to the center position.
            ``p`` : Vertical shift from the ternary axis in the `display`
            coordinate system. ``p > 0`` and ``p < 0`` are towards the outside
            and the inside of the triangle.

        Returns
        -------
        (x, y) : Coordinates in the `display` (pixel) coordinates.
        """
        c0, c1, c2 = self.trans.transform([[1.0, 0.5], [0.0, 0.0], [0.0, 1.0]])
        v02 = c2 - c0
        v21 = c1 - c2
        # Obtain the vector perpendicular to v12 in the Gram-Schmidt method.
        # The obtained `vp` points inside of the triangle, regardless if the
        # triangle is defined in a clockwise or in a counterclockwise manner.
        vp = v02 - np.dot(v02, v21) / np.dot(v21, v21) * v21
        vp /= np.linalg.norm(vp)
        return np.array([
            [v21[0], vp[0], c2[0]],
            [v21[1], vp[1], c2[1]],
            [0.0, 0.0, 1.0],
        ])

    def inverted(self):
        self._invalid = 1  # necessary to recompute the inverted transform
        return super().inverted()


class PCTransform(Affine2DBase):
    """Transform to place axis-label at corner.

    Parameters
    ----------
    trans : ``Transform``
        Transform derived from ``TernaryTransform`` is supposed to be given.
    """
    input_dims = 2
    output_dims = 2

    def __init__(self, trans: Transform, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans

    def get_matrix(self):
        """Transform axis-label to Cartesian (likely `display`) coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            ``s, p == values[:, 0], values[:, 1]``
            ``s`` : coordinate along the the edge opposite to the vertex.
            ``s == 0.5`` corresponds to the corner position.
            ``p`` : Vertical shift from the first axis in the `display`
            coordinate system. ``p > 0`` and ``p < 0`` are towards the outside
            and the inside of the triangle.

        Returns
        -------
        (x, y) : Coordinates in the `display` (pixel) coordinates.
        """
        c0, c1, c2 = self.trans.transform([[1.0, 0.5], [0.0, 0.0], [0.0, 1.0]])
        v10 = c0 - c1
        v12 = c2 - c1
        # Obtain the vector perpendicular to v21 in the Gram-Schmidt method.
        # The obtained `vp` points inside of the triangle, regardless if the
        # triangle is defined in a clockwise or in a counterclockwise manner.
        vp = v10 - np.dot(v10, v12) / np.dot(v12, v12) * v12
        vp /= np.linalg.norm(vp)
        return np.array([
            [v12[0], vp[0], c0[0] - 0.5 * v12[0]],
            [v12[1], vp[1], c0[1] - 0.5 * v12[1]],
            [0.0, 0.0, 1.0],
        ])

    def inverted(self):
        self._invalid = 1  # necessary to recompute the inverted transform
        return super().inverted()


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


class T2HWidthTransform(Transform):
    """Transform from ternary-axis to scaled hexagonal-axis coordinates."""
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, ternary_scale, viewTernaryLims, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_scale = ternary_scale
        self.viewTernaryLims = viewTernaryLims
        self.index = index

    def transform_non_affine(self, values):
        """Transform ternary-axis to scaled hexagonal-axis coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            Coordinates in the ternary-axis coordinates.
            ``s, p == values[:, 0], values[:, 1]``
            ``s`` : ternary coordinate of the given axis.
            ``s == ternary_min`` and ``s == ternary_max`` correspond to the
            side and the corner of the extrapolative triangle, respectively.
            ``p == 0`` and ``p == 1`` correspond to the end points of the edge.

        Returns
        -------
        (x, y) : (N, 2) array_like
            Coordinates in the scaled hexagonal-axis coordinates.
            ``x == 0`` corresponds to the side of the hexagon.
            ``x == 1`` corresponds to the corner of the hexagon.
            ``y == 0`` and ``y == 1`` correspond to the end points of the edge.
        """
        values = np.asarray(values)
        scale = self.ternary_scale
        min0, max0 = self.viewTernaryLims[(self.index + 0) % 3].intervalx
        min1, max1 = self.viewTernaryLims[(self.index + 1) % 3].intervalx
        min2, max2 = self.viewTernaryLims[(self.index - 1) % 3].intervalx
        x = values[:, 0] * ((scale - min1 - min2) - min0) + min0  # unscaling
        denominator = scale - min1 - min2 - x
        y0 = 1.0 - (max2 - min2) / denominator
        y1 = 0.0 + (max1 - min1) / denominator
        sign = np.sign(scale)
        y0 = np.where(sign * (x - (scale - max2 - min1)) > 0.0, 0.0, y0)
        y1 = np.where(sign * (x - (scale - max1 - min2)) > 0.0, 1.0, y1)
        y = (values[:, 1] - y0) / (y1 - y0)
        return np.column_stack((values[:, 0], y))

    def inverted(self):
        return H2TWidthTransform(
            self.ternary_scale, self.viewTernaryLims, self.index)


class H2TWidthTransform(Transform):
    """Transform from scaled hexagonal-axis to ternary-axis coordinates."""
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, ternary_scale, viewTernaryLims, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_scale = ternary_scale
        self.viewTernaryLims = viewTernaryLims
        self.index = index

    def transform_non_affine(self, values):
        """Transform scaled hexagonal-axis to ternary-axis coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            Coordinates in the scaled hexagonal-axis coordinates.
            ``s, p == values[:, 0], values[:, 1]``
            ``s == 0`` corresponds to the side of the hexagon.
            ``s == 1`` corresponds to the corner of the hexagon.
            ``p == 0`` and ``p == 1`` correspond to the end points of the edge.

        Returns
        -------
        (x, y) : (N, 2) array_like
            Coordinates in the ternary-axis coordinates.
            ``x`` : ternary coordinate of the given axis.
            ``x == ternary_min`` and ``x == ternary_max`` correspond to the
            side and the corner of the extrapolative triangle, respectively.
            ``y == 0`` and ``y == 1`` correspond to the end points of the edge.
        """
        values = np.asarray(values)
        scale = self.ternary_scale
        min0, max0 = self.viewTernaryLims[(self.index + 0) % 3].intervalx
        min1, max1 = self.viewTernaryLims[(self.index + 1) % 3].intervalx
        min2, max2 = self.viewTernaryLims[(self.index - 1) % 3].intervalx
        x = values[:, 0] * ((scale - min1 - min2) - min0) + min0  # unscaling
        denominator = scale - min1 - min2 - x
        y0 = 1.0 - (max2 - min2) / denominator
        y1 = 0.0 + (max1 - min1) / denominator
        sign = np.sign(scale)
        y0 = np.where(sign * (x - (scale - max2 - min1)) > 0.0, 0.0, y0)
        y1 = np.where(sign * (x - (scale - max1 - min2)) > 0.0, 1.0, y1)
        y = values[:, 1] * (y1 - y0) + y0
        return np.column_stack((values[:, 0], y))

    def inverted(self):
        return T2HWidthTransform(
            self.ternary_scale, self.viewTernaryLims, self.index)
