import math

import numpy as np

import matplotlib as mpl
import matplotlib.transforms as mtransforms
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib import _api
from mpltern.ternary.transforms import BarycentricTransform
from mpltern.ternary._base import _create_corners
from mpltern._ternary_parsers import _get_xy


class TernaryAxes3D(Axes3D):
    name = 'ternary3d'

    def __init__(self, *args, ternary_sum: float = 1.0, corners=None,
                 rotation: float = None, **kwargs):
        """3D ternary axes object.

        Parameters
        ----------
        ternary_sum : float, optional
            Constant to which ``t + l + r`` is normalized, by default 1.0
        corners : Sequence[float] or None, optional
            Corners of the triangle, by default None
        rotation : float or None, optional
            Rotation angle of the triangle, by default None
        """
        # Since Matplotlib 3.5.0, `auto_add_to_figure` is "deprecated" but
        # actually causes an error if it is `True`.
        # To avoid this we set `False` to this argument.
        # Since Matplotlib 3.6.0, `auto_add_to_figure` is not necessary to set.
        kwargs.setdefault('auto_add_to_figure', False)

        # Triangle corners in the original data coordinates
        self.corners_data = _create_corners(corners, rotation)
        sx = np.sqrt(3.0) * 0.5  # Scale for x
        xmin = -1.0 / np.sqrt(3.0)
        v = xmin * sx
        trans = mtransforms.Affine2D().from_values(sx, 0.0, 0.0, 1.0, -v, 0.0)
        # Triangle corners in the original ``Axes`` coordinates
        self.corners_axes = trans.transform(self.corners_data)

        self.ternary_sum = ternary_sum
        super().__init__(*args, **kwargs)

        # As of Matplotlib 3.5.0, Axes3D does not support `set_aspect` other
        # than `auto` and therefore we need (1) to set the box aspect and the
        # data limits consistently.
        # Since Matplotlib 3.6.0, `set_aspect='equalxy'` can be used.
        self.set_box_aspect((4.0 * 2.0 / math.sqrt(3.0), 4.0, 3.0))

        self.set_ternary_lim(
            0.0, ternary_sum,
            0.0, ternary_sum,
            0.0, ternary_sum,
        )

    def set_figure(self, fig):
        self.viewTLim = mtransforms.Bbox.unit()
        self.viewLLim = mtransforms.Bbox.unit()
        self.viewRLim = mtransforms.Bbox.unit()
        self.viewOuterTLim = mtransforms.Bbox.unit()
        self.viewOuterLLim = mtransforms.Bbox.unit()
        self.viewOuterRLim = mtransforms.Bbox.unit()
        super().set_figure(fig)

    def _set_lim_and_transforms(self):
        super()._set_lim_and_transforms()

        corners_axes = self.corners_axes

        # From ternary coordinates to the original data coordinates
        self.transProjection = BarycentricTransform(self.corners_data)

        # From barycentric coordinates to the original Axes coordinates
        self.transAxesProjection = BarycentricTransform(corners_axes.copy())

        # From barycentric coordinates to display coordinates
        self.transTernaryAxes = self.transAxesProjection + self.transAxes

    def clear(self):
        self.viewTLim.intervalx = 0.0, self.ternary_sum
        self.viewLLim.intervalx = 0.0, self.ternary_sum
        self.viewRLim.intervalx = 0.0, self.ternary_sum
        if tuple(int(_) for _ in mpl.__version__.split('.'))[:2] < (3, 6):
            super().cla()
        else:
            super().clear()
        xmin = -1.0 / np.sqrt(3.0)
        xmax = +1.0 / np.sqrt(3.0)
        self.set_xlim(xmin, xmax)
        self.set_ylim(0.0, 1.0)

    if tuple(int(_) for _ in mpl.__version__.split('.'))[:2] < (3, 6):
        cla = clear

    def _get_hexagonal_vertices(self):
        """Get vertices of the view-limit hexagon."""
        tmin, tmax = self.get_tlim()
        lmin, lmax = self.get_llim()
        rmin, rmax = self.get_rlim()
        return [
            [tmax, lmin, self.ternary_sum - tmax - lmin],
            [tmax, self.ternary_sum - tmax - rmin, rmin],
            [self.ternary_sum - lmax - rmin, lmax, rmin],
            [tmin, lmax, self.ternary_sum - lmax - tmin],
            [tmin, self.ternary_sum - rmax - tmin, rmax],
            [self.ternary_sum - rmax - lmin, lmin, rmax],
        ]

    def _get_triangular_vertices(self):
        """Get vertices of the extrapolative triangle."""
        tmin = self.get_tlim()[0]
        lmin = self.get_llim()[0]
        rmin = self.get_rlim()[0]
        return [
            [self.ternary_sum - lmin - rmin, lmin, rmin],
            [tmin, self.ternary_sum - rmin - tmin, rmin],
            [tmin, lmin, self.ternary_sum - tmin - lmin],
        ]

    def _create_bbox_from_ternary_lim(self, fit: str = "rectangle"):
        if fit == "rectangle":
            tlr = self._get_hexagonal_vertices()
        elif fit == "triangle":
            tlr = self._get_triangular_vertices()
        elif fit == "none":
            tlr = [
                [self.ternary_sum, 0.0, 0.0],
                [0.0, self.ternary_sum, 0.0],
                [0.0, 0.0, self.ternary_sum],
            ]
        else:
            raise ValueError(f'unknown fit: {fit}')
        xy = self.transProjection.transform(tlr)
        bbox = mtransforms.Bbox.unit()
        bbox.update_from_data_xy(xy, ignore=True)
        return bbox

    def set_ternary_lim(
        self, tmin, tmax, lmin, lmax, rmin, rmax, fit: str = "rectangle"
    ):
        """Set ternary limits.

        Parameters
        ----------
        fit : {"rectangle", "triangle", "none"}
            To what the plotting region is fitted.

            - ``'rectangle'``: Fitted to the original rectangle.
            - ``'triangle'``: Fitted to the original triangle.
            - ``'none'``: The plotting region is simply cropped (or expanded).
        """
        _api.check_in_list(['rectangle', 'triangle', 'none'], fit=fit)
        if np.sign(tmax - tmin) != np.sign(self.ternary_sum):
            tmin, tmax = tmax, tmin
        if np.sign(lmax - lmin) != np.sign(self.ternary_sum):
            lmin, lmax = lmax, lmin
        if np.sign(rmax - rmin) != np.sign(self.ternary_sum):
            rmin, rmax = rmax, rmin

        self._set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax)

    def _set_ternary_lim(self, tmin, tmax, lmin, lmax, rmin, rmax):
        """Set ternary limits.

        Notes
        -----
        The given ternary limits may be further modified to show intersections
        of (tmin, tmax), (lmin, lmax), (rmin, rmax).
        """
        tn_sum = self.ternary_sum

        select_min, select_max = (max, min) if tn_sum > 0.0 else (min, max)

        tmin = select_min(tmin, tn_sum - lmax - rmax)
        lmin = select_min(lmin, tn_sum - rmax - tmax)
        rmin = select_min(rmin, tn_sum - tmax - lmax)

        tmax = select_max(tmax, tn_sum - lmin - rmin)
        lmax = select_max(lmax, tn_sum - rmin - tmin)
        rmax = select_max(rmax, tn_sum - tmin - lmin)

        self.viewTLim.intervalx = tmin, tmax
        self.viewLLim.intervalx = lmin, lmax
        self.viewRLim.intervalx = rmin, rmax

        self.viewOuterTLim.intervalx = tmin, tn_sum - lmin - rmin
        self.viewOuterLLim.intervalx = lmin, tn_sum - tmin - rmin
        self.viewOuterRLim.intervalx = rmin, tn_sum - tmin - lmin

    def set_ternary_min(self, tmin, lmin, rmin, fit: str = "rectangle"):
        """Set the minimum values for ternary limits."""
        tmax = self.ternary_sum - lmin - rmin
        lmax = self.ternary_sum - rmin - tmin
        rmax = self.ternary_sum - tmin - lmin
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax, fit)

    def set_ternary_max(self, tmax, lmax, rmax, fit: str = "rectangle"):
        """Set the maximum values for ternary limits."""
        tmin = (self.ternary_sum + tmax - lmax - rmax) * 0.5
        lmin = (self.ternary_sum + lmax - rmax - tmax) * 0.5
        rmin = (self.ternary_sum + rmax - tmax - lmax) * 0.5
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax, fit)

    def get_tlim(self):
        """Return the t-axis view limits."""
        return tuple(self.viewTLim.intervalx)

    def get_llim(self):
        """Return the l-axis view limits."""
        return tuple(self.viewLLim.intervalx)

    def get_rlim(self):
        """Return the r-axis view limits."""
        return tuple(self.viewRLim.intervalx)

    def set_tlim(self, tmin, tmax, fit: str = "rectangle"):
        """Set the t-axis view limits."""
        lmin, lmax = self.get_llim()
        rmin, rmax = self.get_rlim()
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax, fit)
        return self.get_tlim()

    def set_llim(self, lmin, lmax, fit: str = "rectangle"):
        """Set the l-axis view limits."""
        tmin, tmax = self.get_tlim()
        rmin, rmax = self.get_rlim()
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax, fit)
        return self.get_llim()

    def set_rlim(self, rmin, rmax, fit: str = "rectangle"):
        """Set the r-axis view limits."""
        tmin, tmax = self.get_tlim()
        lmin, lmax = self.get_llim()
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax, fit)
        return self.get_rlim()

    def plot(self, *args, **kwargs):
        trans = kwargs.pop('transform', None)
        this, args = args[:3], args[3:]
        x, y, kwargs['transform'] = _get_xy(self, this, trans)
        args = (x, y, *args)
        return super().plot(*args, **kwargs)
