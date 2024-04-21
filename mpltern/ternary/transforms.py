"""
Transforms used for ternary plots.

Notes
-----
Inside ``Transform.transform`` of Matplotlib, the last dimension of the input
values are forced to be the same as ``input_dims``.
"""
import numpy as np

from matplotlib.transforms import Affine2DBase, Transform


class TernaryLinearTransform(Transform):
    """Transform to modify ternary coordinates.

    Its inverse is particularly important to get back the original ternary
    coordinates from barycentric coordinates.

    Parameters
    ----------
    ternary_sum : float
        Value by which ternary coordinates are divided to be suitable for the
        input to BarycentricTransform.
    """
    input_dims = output_dims = 3
    has_inverse = True

    def __init__(self, ternary_sum: float, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_sum = ternary_sum

    def transform_non_affine(self, values):
        """Transform ternary coordinates.

        Parameters
        ----------
        values : (N, 3) array_like
            Ternary coordinates before division.

        Returns
        -------
        (N, 3) np.ndarray
            Ternary coordinates after division.
        """
        return values / self.ternary_sum

    def inverted(self):
        return TernaryLinearTransform(1.0 / self.ternary_sum)


class TernaryAxisTransform(Transform):
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

    def __init__(self, corners, index: int, *args, **kwargs):
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
        corner0 = self.corners[(self.index + 0) % 3]
        corner1 = self.corners[(self.index + 1) % 3]
        corner2 = self.corners[(self.index + 2) % 3]
        s = values[:, 0]
        p = values[:, 1]
        v01 = corner1 - corner0
        v02 = corner2 - corner0
        x = corner0[0] + (1.0 - s) * (p * v01[0] + (1.0 - p) * v02[0])
        y = corner0[1] + (1.0 - s) * (p * v01[1] + (1.0 - p) * v02[1])
        return np.column_stack((x, y)).astype(float)

    def inverted(self):
        return InvertedTernaryAxisTransform(self.corners, self.index)


class InvertedTernaryAxisTransform(Transform):
    """Transform convenient for ticks in TernaryAxis."""
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, corners, index: int, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.corners = np.asarray(corners, float)
        self.index = index

    def transform_non_affine(self, values):
        corner0 = self.corners[(self.index + 0) % 3]
        corner1 = self.corners[(self.index + 1) % 3]
        corner2 = self.corners[(self.index + 2) % 3]
        vectors = np.column_stack((corner1 - corner0, corner2 - corner0))
        relative_points = values - corner0
        tmp = np.linalg.inv(vectors) @ relative_points.T
        s = 1.0 - (tmp[0] + tmp[1])
        p = tmp[0] / (1.0 - s)
        return np.column_stack((s, p)).astype(float)

    def inverted(self):
        return TernaryAxisTransform(self.corners, self.index)


class TernaryTickLabelShift(Affine2DBase):
    """Shift of tick labels from tick points

    This is essentially a wrapper of ScaledTranslation, but the direction to
    pad is determined on the fly when drawing.
    """
    def __init__(self, axes, pad_points: float, indices):
        super().__init__()
        self.axes = axes
        self.pad_points = pad_points
        self.indices = indices

    def get_matrix(self):
        figure = self.axes.figure
        corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
        points = self.axes.transTernaryAxes.transform(corners)[self.indices]
        direction = points[1] - points[0]  # outward against the triangle
        xt, yt = direction / np.linalg.norm(direction) * self.pad_points / 72.0
        xt, yt = figure.dpi_scale_trans.transform((xt, yt))
        return np.array([[1.0, 0.0, xt], [0.0, 1.0, yt], [0.0, 0.0, 1.0]])

    def inverted(self):
        self._invalid = 1  # necessary to recompute the inverted transform
        return super().inverted()


class TernaryAxisLabelSTransform(Affine2DBase):
    """Transform to place axis-label at side.

    Parameters
    ----------
    trans : ``Transform``
        Transform derived from ``TernaryTransform`` is supposed to be given.
    """
    def __init__(self, trans: Transform, h2t: Transform, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans
        self.h2t = h2t

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
        corners = [[1.0, 0.5], [0.0, 1.0], [0.0, 0.0]]
        corner0, corner1, corner2 = self.trans.transform(corners)
        v02 = corner2 - corner0
        v21 = corner1 - corner2
        # Obtain the vector perpendicular to v12 in the Gram-Schmidt method.
        # The obtained `vp` points outside of the triangle, regardless if the
        # triangle is defined in a clockwise or in a counterclockwise manner.
        vperp = v02 - np.dot(v02, v21) / np.dot(v21, v21) * v21
        vperp /= np.linalg.norm(vperp)
        origin = self.trans.transform(self.h2t.transform((0.0, 0.5)))
        return np.array([
            [v21[0], vperp[0], origin[0] - 0.5 * v21[0]],
            [v21[1], vperp[1], origin[1] - 0.5 * v21[1]],
            [0.0, 0.0, 1.0],
        ])

    def inverted(self):
        self._invalid = 1  # necessary to recompute the inverted transform
        return super().inverted()


class TernaryAxisLabelCTransform(Affine2DBase):
    """Transform to place axis-label at corner.

    Parameters
    ----------
    trans : ``Transform``
        Transform derived from ``TernaryTransform`` is supposed to be given.
    """
    def __init__(self, trans: Transform, h2t: Transform, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trans = trans
        self.h2t = h2t

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
        corners = [[1.0, 0.5], [0.0, 1.0], [0.0, 0.0]]
        corner0, corner1, corner2 = self.trans.transform(corners)
        v10 = corner0 - corner1
        v12 = corner2 - corner1
        # Obtain the vector perpendicular to v21 in the Gram-Schmidt method.
        # The obtained `vp` points outside of the triangle, regardless if the
        # triangle is defined in a clockwise or in a counterclockwise manner.
        vperp = v10 - np.dot(v10, v12) / np.dot(v12, v12) * v12
        vperp /= np.linalg.norm(vperp)
        origin = self.trans.transform(self.h2t.transform((1.0, 0.5)))
        return np.array([
            [v12[0], vperp[0], origin[0] - 0.5 * v12[0]],
            [v12[1], vperp[1], origin[1] - 0.5 * v12[1]],
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
        """Transform barycentric to Cartesian coordinates

        Parameters
        ----------
        values : (N, 3) array_like
            Points in the barycentric coordinates.

        Returns
        -------
        (x, y) : Cartesian coordinates
        """
        return (values / np.sum(values, axis=1)[:, None]) @ self.corners

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


class H2THeightTransform(Transform):
    """Transform from scaled hexagonal-axis to ternary-axis coordinates."""
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, ternary_sum: float, viewTernaryLims: list, index: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_sum = ternary_sum
        self.viewTernaryLims = viewTernaryLims
        self.index = index

    def transform_non_affine(self, values):
        """Transform scaled hexagonal-axis to ternary-axis coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            Coordinates in the scaled hexagonal-axis coordinates.
            ``s, p == values[:, 0], values[:, 1]``
            ``s == 0`` corresponds to the bottom of the hexagon.
            ``s == 1`` corresponds to the top of the hexagon.
            ``p`` is not modified.

        Returns
        -------
        (x, y) : (N, 2) array_like
            Coordinates in the ternary-axis coordinates.
            ``x == 0`` corresponds to the bottom of the extrapolative triangle.
            ``x == 1`` corresponds to the top of the extrapolative triangle.
            ``y`` is equal to ``p``.
        """
        values = np.asarray(values)
        tn_sum = self.ternary_sum
        min0, max0 = self.viewTernaryLims[(self.index + 0) % 3].intervalx
        min1, max1 = self.viewTernaryLims[(self.index + 1) % 3].intervalx
        min2, max2 = self.viewTernaryLims[(self.index - 1) % 3].intervalx

        x = values[:, 0] * (max0 - min0) + min0  # unscale
        x = (x - min0) / ((tn_sum - min1 - min2) - min0)  # rescale

        return np.column_stack((x, values[:, 1]))

    def inverted(self):
        return T2HHeightTransform(
            self.ternary_sum, self.viewTernaryLims, self.index)


class T2HHeightTransform(Transform):
    """Transform from scaled hexagonal-axis to ternary-axis coordinates."""
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, ternary_sum: float, viewTernaryLims: list, index: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_sum = ternary_sum
        self.viewTernaryLims = viewTernaryLims
        self.index = index

    def transform_non_affine(self, values):
        """Transform scaled hexagonal-axis to ternary-axis coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            Coordinates in the scaled hexagonal-axis coordinates.
            ``s, p == values[:, 0], values[:, 1]``
            ``s == 0`` corresponds to the bottom of the extrapolative triangle.
            ``s == 1`` corresponds to the top of the extrapolative triangle.
            ``p`` is not modified.

        Returns
        -------
        (x, y) : (N, 2) array_like
            Coordinates in the ternary-axis coordinates.
            ``x == 0`` corresponds to the bottom of the hexagon.
            ``x == 1`` corresponds to the top of the hexagon.
            ``y`` is equal to ``p``.
        """
        values = np.asarray(values)
        tn_sum = self.ternary_sum
        min0, max0 = self.viewTernaryLims[(self.index + 0) % 3].intervalx
        min1, max1 = self.viewTernaryLims[(self.index + 1) % 3].intervalx
        min2, max2 = self.viewTernaryLims[(self.index - 1) % 3].intervalx

        x = values[:, 0] * ((tn_sum - min1 - min2) - min0) + min0  # unscale
        x = (x - min0) / (max0 - min0)  # rescale

        return np.column_stack((x, values[:, 1]))

    def inverted(self):
        return H2THeightTransform(
            self.ternary_sum, self.viewTernaryLims, self.index)


class T2HWidthTransform(Transform):
    """Transform from ternary-axis to scaled hexagonal-axis coordinates."""
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, ternary_sum: float, viewTernaryLims: list, index: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_sum = ternary_sum
        self.viewTernaryLims = viewTernaryLims
        self.index = index

    def transform_non_affine(self, values):
        """Transform ternary-axis to scaled hexagonal-axis coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            Coordinates in the ternary-axis coordinates.
            ``s, p == values[:, 0], values[:, 1]``
            ``s`` is not modified.
            ``p == 0`` and ``p == 1`` correspond to the end points of the edge.

        Returns
        -------
        (x, y) : (N, 2) array_like
            Coordinates in the scaled hexagonal-axis coordinates.
            ``x`` is equal to ``s``.
            ``y == 0`` and ``y == 1`` correspond to the end points of the edge.
        """
        values = np.asarray(values)
        tn_sum = self.ternary_sum
        min0, max0 = self.viewTernaryLims[(self.index + 0) % 3].intervalx
        min1, max1 = self.viewTernaryLims[(self.index + 1) % 3].intervalx
        min2, max2 = self.viewTernaryLims[(self.index - 1) % 3].intervalx

        x = values[:, 0] * ((tn_sum - min1 - min2) - min0) + min0  # unscale

        denominator = tn_sum - min1 - min2 - x
        out = np.zeros_like(denominator)
        where = (denominator != 0.0)
        y0 = 1.0 - np.divide(max2 - min2, denominator, out=out, where=where)
        y1 = 0.0 + np.divide(max1 - min1, denominator, out=out, where=where)

        sign = np.sign(tn_sum)
        y0 = np.where(sign * (x - (tn_sum - max2 - min1)) > 0.0, 0.0, y0)
        y1 = np.where(sign * (x - (tn_sum - max1 - min2)) > 0.0, 1.0, y1)
        y = (values[:, 1] - y0) / (y1 - y0)

        return np.column_stack((values[:, 0], y))

    def inverted(self):
        return H2TWidthTransform(
            self.ternary_sum, self.viewTernaryLims, self.index)


class H2TWidthTransform(Transform):
    """Transform from scaled hexagonal-axis to ternary-axis coordinates."""
    input_dims = 2
    output_dims = 2
    has_inverse = True

    def __init__(self, ternary_sum: float, viewTernaryLims: list, index: int,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ternary_sum = ternary_sum
        self.viewTernaryLims = viewTernaryLims
        self.index = index

    def transform_non_affine(self, values):
        """Transform scaled hexagonal-axis to ternary-axis coordinates

        Parameters
        ----------
        values : (N, 2) array_like
            Coordinates in the scaled hexagonal-axis coordinates.
            ``s, p == values[:, 0], values[:, 1]``
            ``s`` is not modified.
            ``p == 0`` and ``p == 1`` correspond to the end points of the edge.

        Returns
        -------
        (x, y) : (N, 2) array_like
            Coordinates in the ternary-axis coordinates.
            ``x`` is equal to ``s``.
            ``y == 0`` and ``y == 1`` correspond to the end points of the edge.
        """
        values = np.asarray(values)
        tn_sum = self.ternary_sum
        min0, max0 = self.viewTernaryLims[(self.index + 0) % 3].intervalx
        min1, max1 = self.viewTernaryLims[(self.index + 1) % 3].intervalx
        min2, max2 = self.viewTernaryLims[(self.index - 1) % 3].intervalx

        x = values[:, 0] * ((tn_sum - min1 - min2) - min0) + min0  # unscale

        denominator = tn_sum - min1 - min2 - x
        out = np.zeros_like(denominator)
        where = (denominator != 0.0)
        y0 = 1.0 - np.divide(max2 - min2, denominator, out=out, where=where)
        y1 = 0.0 + np.divide(max1 - min1, denominator, out=out, where=where)

        sign = np.sign(tn_sum)
        y0 = np.where(sign * (x - (tn_sum - max2 - min1)) > 0.0, 0.0, y0)
        y1 = np.where(sign * (x - (tn_sum - max1 - min2)) > 0.0, 1.0, y1)
        y = values[:, 1] * (y1 - y0) + y0

        return np.column_stack((values[:, 0], y))

    def inverted(self):
        return T2HWidthTransform(
            self.ternary_sum, self.viewTernaryLims, self.index)
