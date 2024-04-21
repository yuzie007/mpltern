import logging
import warnings

import numpy as np

import matplotlib as mpl
import matplotlib.cbook as cbook
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.axis as maxis
from matplotlib.axes import Axes
from matplotlib import _api
from mpltern.ternary.spines import Spine
from mpltern.ternary.transforms import (
    TernaryAxisTransform, TernaryTickLabelShift,
    TernaryAxisLabelSTransform, TernaryAxisLabelCTransform,
    H2THeightTransform, H2TWidthTransform,
    TernaryLinearTransform,
    BarycentricTransform)
from mpltern.ternary.axis import TAxis, LAxis, RAxis

_log = logging.getLogger(__name__)


def _create_corners(corners=None, rotation=None):
    if corners is None:
        # By default, regular upward triangle is created.
        # The bottom and the top of the triangle have 0.0 and 1.0,
        # respectively, as the *y* coordinate in the original `Axes`
        # coordinates.
        # The horizontal center of the triangle has 0.0 as the *x*
        # coordinate in the original `Axes` coordinates.
        # The other coordinates are given to make the regular triangle.
        xmin = -1.0 / np.sqrt(3.0)
        xmax = +1.0 / np.sqrt(3.0)
        corners = ((0.0, 1.0), (xmin, 0.0), (xmax, 0.0))
    corners = np.asarray(corners)
    if rotation is not None:
        # The rotation is done around the centroid of the given triangle.
        cx, cy = np.average(corners, axis=0)
        trans = mtransforms.Affine2D().rotate_deg_around(cx, cy, rotation)
        corners = trans.transform(corners)
        # The following shift places the triangle inside the original
        # square `Axes` as much as possible.
        tmp = (np.min(corners, axis=0) + np.max(corners, axis=0)) * 0.5
        corners += (np.array([0.0, 0.5]) - tmp)
    return corners


class TernaryAxesBase(Axes):
    _axis_names = ("x", "y", "t", "l", "r")
    _shared_axes = {name: cbook.Grouper() for name in _axis_names}

    def __init__(self, *args, ternary_sum: float = 1.0, corners=None,
                 rotation: float = None, **kwargs):
        """Build an TernaryAxes in a figure.

        Parameters
        ----------
        ternary_sum : float, optional
            Constant to which ``t + l + r`` is normalized, by default 1.0
        corners : Sequence[float] or None, optional
            Corners of the triangle, by default None
        rotation : float or None, optional
            Rotation angle of the triangle, by default None
        """
        if "ternary_scale" in kwargs:
            warnings.warn(
                "Since mpltern 1.0.0, the normalization constant for a "
                "ternary plot has been renamed from `ternary_scale` to "
                "`ternary_sum`. Use the latter."
            )
            ternary_sum = kwargs.pop("ternary_scale")

        # workaround for matplotlib>=3.6.0
        self._sharet = None
        self._sharel = None
        self._sharer = None

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
        self.set_aspect('equal', adjustable='box', anchor='C')
        self.set_ternary_lim(
            0.0, ternary_sum,
            0.0, ternary_sum,
            0.0, ternary_sum,
        )

    @property
    def callbacks(self):
        if tuple(int(_) for _ in mpl.__version__.split('.')[:2]) < (3, 6):
            return cbook.CallbackRegistry()
        else:
            return cbook.CallbackRegistry(
               signals=[f"{name}lim_changed" for name in self._axis_names])

    @callbacks.setter
    def callbacks(self, value):
        pass

    def set_figure(self, fig):
        self.viewTLim = mtransforms.Bbox.unit()
        self.viewLLim = mtransforms.Bbox.unit()
        self.viewRLim = mtransforms.Bbox.unit()
        self.viewOuterTLim = mtransforms.Bbox.unit()
        self.viewOuterLLim = mtransforms.Bbox.unit()
        self.viewOuterRLim = mtransforms.Bbox.unit()
        super().set_figure(fig)

    def _get_axis_list(self):
        return tuple(getattr(self, f"{name}axis") for name in self._axis_names)

    def _get_axis_map(self):
        # workaround for matplotlib>=3.4.0
        d = {}
        axis_list = self._get_axis_list()
        for k, v in vars(self).items():
            if k.endswith("axis") and v in axis_list:
                d[k[:-len("axis")]] = v
        d.update({'x': d['t'], 'y': d['t']})
        return d

    def _init_axis(self):
        self.xaxis = maxis.XAxis(self)
        self.yaxis = maxis.YAxis(self)

        self.xaxis.set_visible(False)
        self.yaxis.set_visible(False)

        self.taxis = TAxis(self)
        self.laxis = LAxis(self)
        self.raxis = RAxis(self)

        self.spines['tside'].register_axis(self.taxis)
        self.spines['lside'].register_axis(self.laxis)
        self.spines['rside'].register_axis(self.raxis)

        self.spines['tcorner'].register_axis(self.taxis)
        self.spines['lcorner'].register_axis(self.laxis)
        self.spines['rcorner'].register_axis(self.raxis)

        self._update_transScale()

    def _set_lim_and_transforms(self):
        super()._set_lim_and_transforms()

        self.transTernaryScale = TernaryLinearTransform(self.ternary_sum)

        transTLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewOuterTLim, self.transScale))
        transLLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewOuterLLim, self.transScale))
        transRLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewOuterRLim, self.transScale))

        corners_axes = self.corners_axes

        ternary_limits = [self.viewTLim, self.viewLLim, self.viewRLim]

        h2t_h_t = H2THeightTransform(self.ternary_sum, ternary_limits, 0)
        h2t_h_l = H2THeightTransform(self.ternary_sum, ternary_limits, 1)
        h2t_h_r = H2THeightTransform(self.ternary_sum, ternary_limits, 2)

        h2t_w_t = H2TWidthTransform(self.ternary_sum, ternary_limits, 0)
        h2t_w_l = H2TWidthTransform(self.ternary_sum, ternary_limits, 1)
        h2t_w_r = H2TWidthTransform(self.ternary_sum, ternary_limits, 2)

        h2t_t = h2t_h_t + h2t_w_t
        h2t_l = h2t_h_l + h2t_w_l
        h2t_r = h2t_h_r + h2t_w_r

        # From scaled ternary-axis coordinates to display coordinates
        taxis_tr = TernaryAxisTransform(corners_axes, 0) + self.transAxes
        laxis_tr = TernaryAxisTransform(corners_axes, 1) + self.transAxes
        raxis_tr = TernaryAxisTransform(corners_axes, 2) + self.transAxes

        # For ticks and spines
        self._taxis_transform = transTLimits + h2t_w_t + taxis_tr
        self._laxis_transform = transLLimits + h2t_w_l + laxis_tr
        self._raxis_transform = transRLimits + h2t_w_r + raxis_tr

        # For axis labels (to display coordinates)
        self._tlabel_s_transform = TernaryAxisLabelSTransform(taxis_tr, h2t_t)
        self._llabel_s_transform = TernaryAxisLabelSTransform(laxis_tr, h2t_l)
        self._rlabel_s_transform = TernaryAxisLabelSTransform(raxis_tr, h2t_r)
        self._tlabel_c_transform = TernaryAxisLabelCTransform(taxis_tr, h2t_t)
        self._llabel_c_transform = TernaryAxisLabelCTransform(laxis_tr, h2t_l)
        self._rlabel_c_transform = TernaryAxisLabelCTransform(raxis_tr, h2t_r)

        # From ternary coordinates to the original data coordinates
        self.transProjection = \
            self.transTernaryScale + BarycentricTransform(self.corners_data)

        # From ternary coordinates to the original Axes coordinates
        self._ternary_axes_transform = self.transProjection + self.transLimits

        # From ternary coordinates to display coordinates
        self._ternary2display_transform = self.transProjection + self.transData

        # From barycentric coordinates to the original Axes coordinates
        self.transAxesProjection = BarycentricTransform(corners_axes.copy())

        # From barycentric coordinates to display coordinates
        self.transTernaryAxes = self.transAxesProjection + self.transAxes

        # From outer Axes coordinates to display coordinates
        self._outer_position = mtransforms.Bbox.unit()
        self.transOuterAxes = (
            mtransforms.BboxTransformTo(self._outer_position) + self.transAxes)

    def get_xaxis_transform(self, which='grid'):
        # Overridden not to call spines
        return self._xaxis_transform

    def get_yaxis_transform(self, which='grid'):
        # Overridden not to call spines
        return self._yaxis_transform

    def get_taxis_transform(self, which='grid'):
        """Get the transformation for drawing t-axis ticks and gridlines."""
        return self._taxis_transform

    def get_laxis_transform(self, which='grid'):
        """Get the transformation for drawing l-axis ticks and gridlines."""
        return self._laxis_transform

    def get_raxis_transform(self, which='grid'):
        """Get the transformation for drawing r-axis ticks and gridlines."""
        return self._raxis_transform

    def _get_axis_text_transform(self, pad_points, trans, indices):
        pad_shift = TernaryTickLabelShift(self, pad_points, indices)
        # `va` and `ha` are modified in `TernaryTick`
        return trans + pad_shift, 'top', 'center'

    def get_taxis_text1_transform(self, pad_points):
        """Get the transformation for drawing t-axis tick-labels."""
        trans = self.get_taxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, [1, 2])

    def get_taxis_text2_transform(self, pad_points):
        """Get the transformation for drawing t-axis tick-labels."""
        trans = self.get_taxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, [2, 1])

    def get_laxis_text1_transform(self, pad_points):
        """Get the transformation for drawing l-axis tick-labels."""
        trans = self.get_laxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, [2, 0])

    def get_laxis_text2_transform(self, pad_points):
        """Get the transformation for drawing l-axis tick-labels."""
        trans = self.get_laxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, [0, 2])

    def get_raxis_text1_transform(self, pad_points):
        """Get the transformation for drawing r-axis tick-labels."""
        trans = self.get_raxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, [0, 1])

    def get_raxis_text2_transform(self, pad_points):
        """Get the transformation for drawing r-axis tick-labels."""
        trans = self.get_raxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, [1, 0])

    def _gen_axes_patch(self):
        return mpatches.Polygon(np.repeat(self.corners_axes, 2, axis=0))

    def _gen_axes_spines(self, locations=None, offset=0.0, units='inches'):
        # overridden to use `Spine` in `mpltern`
        return {side: Spine.linear_spine(self, side) for side in
                ['tside', 'tcorner', 'lside', 'lcorner', 'rside', 'rcorner']}

    def get_taxis(self):
        """Return the TAxis instance"""
        return self.taxis

    def get_laxis(self):
        """Return the LAxis instance"""
        return self.laxis

    def get_raxis(self):
        """Return the RAxis instance"""
        return self.raxis

    def clear(self):
        self.viewTLim.intervalx = 0.0, self.ternary_sum
        self.viewLLim.intervalx = 0.0, self.ternary_sum
        self.viewRLim.intervalx = 0.0, self.ternary_sum
        if tuple(int(_) for _ in mpl.__version__.split('.')[:2]) < (3, 6):
            super().cla()
        else:
            super().clear()
        xmin = -1.0 / np.sqrt(3.0)
        xmax = +1.0 / np.sqrt(3.0)
        self.set_xlim(xmin, xmax)
        self.set_ylim(0.0, 1.0)

    if tuple(int(_) for _ in mpl.__version__.split('.')[:2]) < (3, 6):
        cla = clear

    def autoscale_view(self, *args, **kwargs):
        pass

    def _update_title_position(self, renderer):
        """
        Update the title position based on the bounding box enclosing
        all the ticklabels and x-axis spine and xlabel...
        """
        if self._autotitlepos is not None and not self._autotitlepos:
            _log.debug('title position was updated manually, not adjusting')
            return

        titles = (self.title, self._left_title, self._right_title)

        # Need to check all our twins too, and all the children as well.
        axs = self._twinned_axes.get_siblings(self) + self.child_axes
        for ax in self.child_axes:  # Child positions must be updated first.
            locator = ax.get_axes_locator()
            ax.apply_aspect(locator(self, renderer) if locator else None)

        for title in titles:
            x, _ = title.get_position()
            # need to start again in case of window resizing
            title.set_position((x, 1.0))
            top = -np.inf
            for ax in axs:
                bb = None
                if isinstance(ax, TernaryAxesBase):
                    axis_list = ax._get_axis_map().values()
                else:
                    axis_list = [ax.xaxis]
                for axis in axis_list:
                    bb = axis.get_tightbbox(renderer)
                    if bb is None:
                        bb = ax.get_window_extent(renderer)
                    top = max(top, bb.ymax)
                if title.get_text():
                    if isinstance(ax, TernaryAxesBase):
                        axis_list = ax._get_axis_map().values()
                    else:
                        axis_list = [ax.yaxis]
                    for axis in axis_list:
                        axis.get_tightbbox(renderer)  # update offsetText
                        if axis.offsetText.get_text():
                            bb = axis.offsetText.get_tightbbox(renderer)
                            title_tightbbox = title.get_tightbbox(renderer)
                            if bb.intersection(title_tightbbox, bb):
                                top = bb.ymax
            if top < 0:
                # the top of Axes is not even on the figure, so don't try and
                # automatically place it.
                _log.debug('top of Axes not in the figure, so title not moved')
                return
            if title.get_window_extent(renderer).ymin < top:
                _, y = self.transAxes.inverted().transform((0, top))
                title.set_position((x, y))
                # empirically, this doesn't always get the min to top,
                # so we need to adjust again.
                if title.get_window_extent(renderer).ymin < top:
                    _, y = self.transAxes.inverted().transform(
                        (0., 2 * top - title.get_window_extent(renderer).ymin))
                    title.set_position((x, y))

        ymax = max(title.get_position()[1] for title in titles)
        for title in titles:
            # now line up all the titles at the highest baseline.
            x, _ = title.get_position()
            title.set_position((x, ymax))

    def grid(self, visible=None, which='major', axis='both', **kwargs):
        """
        Configure the grid lines.

        Parameters
        ----------
        visible : bool or None, optional
            Whether to show the grid lines.  If any *kwargs* are supplied, it
            is assumed you want the grid on and *visible* will be set to True.

            If *visible* is *None* and there are no *kwargs*, this toggles the
            visibility of the lines.

        which : {'major', 'minor', 'both'}, optional
            The grid lines to apply the changes on.

        axis : {'both', 't', 'l', 'r'}, optional
            The axis to apply the changes on.

        **kwargs : `.Line2D` properties
            Define the line properties of the grid, e.g.::

                grid(color='r', linestyle='-', linewidth=2)

            Valid keyword arguments are:

            %(Line2D:kwdoc)s

        Notes
        -----
        The axis is drawn as a unit, so the effective zorder for drawing the
        grid is determined by the zorder of each axis, not by the zorder of the
        `.Line2D` objects comprising the grid.  Therefore, to set grid zorder,
        use `.set_axisbelow` or, for more control, call the
        `~.Artist.set_zorder` method of each axis.
        """
        _api.check_in_list(['t', 'l', 'r', 'both'], axis=axis)
        if axis in ['t', 'both']:
            self.taxis.grid(visible, which=which, **kwargs)
        if axis in ['l', 'both']:
            self.laxis.grid(visible, which=which, **kwargs)
        if axis in ['r', 'both']:
            self.raxis.grid(visible, which=which, **kwargs)

    def tick_params(self, axis='both', **kwargs):
        """
        Change the appearance of ticks, tick labels, and gridlines.
        """
        _api.check_in_list(['t', 'l', 'r', 'both'], axis=axis)
        if axis in ['t', 'both']:
            bkw = dict(kwargs)
            bkw.pop('left', None)
            bkw.pop('right', None)
            bkw.pop('labelleft', None)
            bkw.pop('labelright', None)
            self.taxis.set_tick_params(**bkw)
        if axis in ['l', 'both']:
            rkw = dict(kwargs)
            rkw.pop('left', None)
            rkw.pop('right', None)
            rkw.pop('labelleft', None)
            rkw.pop('labelright', None)
            self.laxis.set_tick_params(**rkw)
        if axis in ['r', 'both']:
            lkw = dict(kwargs)
            lkw.pop('left', None)
            lkw.pop('right', None)
            lkw.pop('labelleft', None)
            lkw.pop('labelright', None)
            self.raxis.set_tick_params(**lkw)

    def get_tlabel(self):
        """
        Get the tlabel text string.
        """
        label = self.taxis.get_label()
        return label.get_text()

    def set_tlabel(self, tlabel, fontdict=None, labelpad=None, *,
                   loc=None, **kwargs):
        """
        Set the label for the t-axis.

        Parameters
        ----------
        tlabel : str
            The label text.

        labelpad : float, default: :rc:`axes.labelpad`
            Spacing in points from the Axes bounding box including ticks
            and tick labels.  If None, the previous value is left as is.

        loc : {'left', 'center', 'right'}, default: :rc:`xaxis.labellocation`
            The label position. This is a high-level alternative for passing
            parameters *x* and *horizontalalignment*.

        Other Parameters
        ----------------
        **kwargs : `.Text` properties
            `.Text` properties control the appearance of the label.

        See Also
        --------
        text : Documents the properties supported by `.Text`.
        """
        if labelpad is not None:
            self.taxis.labelpad = labelpad
        protected_kw = ['x', 'horizontalalignment', 'ha']
        if {*kwargs} & {*protected_kw}:
            if loc is not None:
                raise TypeError(f"Specifying 'loc' is disallowed when any of "
                                f"its corresponding low level keyword "
                                f"arguments ({protected_kw}) are also "
                                f"supplied")

        else:
            loc = (loc if loc is not None
                   else mpl.rcParams['xaxis.labellocation'])
            _api.check_in_list(('left', 'center', 'right'), loc=loc)

            x = {
                'left': 0,
                'center': 0.5,
                'right': 1,
            }[loc]
            kwargs.update(x=x, horizontalalignment=loc)

        return self.taxis.set_label_text(tlabel, fontdict, **kwargs)

    def get_llabel(self):
        """
        Get the llabel text string.
        """
        label = self.laxis.get_label()
        return label.get_text()

    def set_llabel(self, llabel, fontdict=None, labelpad=None, *,
                   loc=None, **kwargs):
        """
        Set the label for the l-axis.

        Parameters
        ----------
        llabel : str
            The label text.

        labelpad : float, default: :rc:`axes.labelpad`
            Spacing in points from the Axes bounding box including ticks
            and tick labels.  If None, the previous value is left as is.

        loc : {'left', 'center', 'right'}, default: :rc:`xaxis.labellocation`
            The label position. This is a high-level alternative for passing
            parameters *x* and *horizontalalignment*.

        Other Parameters
        ----------------
        **kwargs : `.Text` properties
            `.Text` properties control the appearance of the label.

        See Also
        --------
        text : Documents the properties supported by `.Text`.
        """
        if labelpad is not None:
            self.laxis.labelpad = labelpad
        protected_kw = ['x', 'horizontalalignment', 'ha']
        if {*kwargs} & {*protected_kw}:
            if loc is not None:
                raise TypeError(f"Specifying 'loc' is disallowed when any of "
                                f"its corresponding low level keyword "
                                f"arguments ({protected_kw}) are also "
                                f"supplied")

        else:
            loc = (loc if loc is not None
                   else mpl.rcParams['xaxis.labellocation'])
            _api.check_in_list(('left', 'center', 'right'), loc=loc)

            x = {
                'left': 0,
                'center': 0.5,
                'right': 1,
            }[loc]
            kwargs.update(x=x, horizontalalignment=loc)

        return self.laxis.set_label_text(llabel, fontdict, **kwargs)

    def get_rlabel(self):
        """
        Get the rlabel text string.
        """
        label = self.raxis.get_label()
        return label.get_text()

    def set_rlabel(self, rlabel, fontdict=None, labelpad=None, *,
                   loc=None, **kwargs):
        """
        Set the label for the r-axis.

        Parameters
        ----------
        rlabel : str
            The label text.

        labelpad : float, default: :rc:`axes.labelpad`
            Spacing in points from the Axes bounding box including ticks
            and tick labels.  If None, the previous value is left as is.

        loc : {'left', 'center', 'right'}, default: :rc:`xaxis.labellocation`
            The label position. This is a high-level alternative for passing
            parameters *x* and *horizontalalignment*.

        Other Parameters
        ----------------
        **kwargs : `.Text` properties
            `.Text` properties control the appearance of the label.

        See Also
        --------
        text : Documents the properties supported by `.Text`.
        """
        if labelpad is not None:
            self.raxis.labelpad = labelpad
        protected_kw = ['x', 'horizontalalignment', 'ha']
        if {*kwargs} & {*protected_kw}:
            if loc is not None:
                raise TypeError(f"Specifying 'loc' is disallowed when any of "
                                f"its corresponding low level keyword "
                                f"arguments ({protected_kw}) are also "
                                f"supplied")

        else:
            loc = (loc if loc is not None
                   else mpl.rcParams['xaxis.labellocation'])
            _api.check_in_list(('left', 'center', 'right'), loc=loc)

            x = {
                'left': 0,
                'center': 0.5,
                'right': 1,
            }[loc]
            kwargs.update(x=x, horizontalalignment=loc)

        return self.raxis.set_label_text(rlabel, fontdict, **kwargs)

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

        boxin = self._create_bbox_from_ternary_lim("none")

        self._set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax)

        boxout = self._create_bbox_from_ternary_lim(fit)

        trans = mtransforms.BboxTransform(boxin, boxout)

        points = [[-0.5 / np.sqrt(3.0), 0.0], [+0.5 / np.sqrt(3.0), 1.0]]

        # Expand xlim or ylim to keep:
        # - the original Axes ratio
        # - the same x/y aspect (by default equal, modified by set_aspect)
        # - the position of the hexagon to the center of Axes
        bbox = mtransforms.Bbox.unit()
        bbox.update_from_data_xy(trans.transform(points))
        aspect = 0.5 * np.sqrt(3.0)
        if isinstance(self.get_aspect(), float):
            aspect *= self.get_aspect()
        tmp = aspect / (bbox.height / bbox.width)
        if bbox.height / bbox.width < aspect:
            bbox = bbox.expanded(1.0, tmp)
        else:
            bbox = bbox.expanded(1.0 / tmp, 1.0)
        self.set_xlim(bbox.x0, bbox.x1)
        self.set_ylim(bbox.y0, bbox.y1)

        self._update_axes_patch()
        self._update_triangular_vertices()

    def _update_axes_patch(self):
        tlr = self._get_hexagonal_vertices()
        xy = self._ternary_axes_transform.transform(tlr)
        self.patch.set_xy(xy)

    def _update_triangular_vertices(self):
        tlr = self._get_triangular_vertices()
        xy = self._ternary_axes_transform.transform(tlr)
        # Update the corner positions in axes coordinates.
        # Indexing is necessary to keep the object ID.
        self.corners_axes[:, :] = xy
        self._outer_position.update_from_data_xy(xy)

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

    # Interactive manipulation

    def can_zoom(self):
        """
        Return whether this Axes supports the zoom box button functionality.

        TernaryAxes does not support zoom boxes.
        """
        return False

    def _set_view(self, view):
        super()._set_view(view)
        self._set_ternary_lim_from_xlim_and_ylim()

    # def _set_view_from_bbox(self, *args, **kwargs):
    #     super()._set_view_from_bbox(*args, **kwargs)
    #     self._set_ternary_lim_from_xlim_and_ylim()

    def drag_pan(self, *args, **kwargs):
        super().drag_pan(*args, **kwargs)
        self._set_ternary_lim_from_xlim_and_ylim()

    def _set_ternary_lim_from_xlim_and_ylim(self):
        """Set ternary lim from xlim and ylim in the interactive mode.

        This is called from
        - _set_view (`Home`, `Forward`, `Backward`)
        - _set_view_from_bbox (`Zoom-to-rectangle`)
        - drag_pan (`Pan/Zoom`)
        (https://matplotlib.org/users/navigation_toolbar.html)
        """
        # points = self.transProjection.inverted().transform(self.corners)
        trans = self._ternary_axes_transform.inverted()
        points = trans.transform(self.patch.get_xy())

        tmax = points[0, 0]
        tmin = points[3, 0]
        lmax = points[2, 1]
        lmin = points[5, 1]
        rmax = points[4, 2]
        rmin = points[1, 2]

        self._set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax)
