import logging

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
    TernaryTransform, TernaryPerpendicularTransform,
    BarycentricTransform, TernaryScaleTransform, TernaryShift)
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

    def __init__(self, *args, ternary_scale=1.0, corners=None, rotation=None,
                 **kwargs):
        """Build an TernaryAxes in a figure.

        Parameters
        ----------
        ternary_scale : float, optional
            ``t + l + r``, by default 1.0
        corners : Sequence[float] or None, optional
            Corners of the triangle, by default None
        rotation : float or None, optional
            Rotation angle of the triangle, by default None
        """
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

        self.ternary_scale = ternary_scale
        super().__init__(*args, **kwargs)
        self.set_aspect('equal', adjustable='box', anchor='C')
        self.set_ternary_lim(
            0.0, ternary_scale, 0.0, ternary_scale, 0.0, ternary_scale)

    @property
    def callbacks(self):
        if tuple(int(_) for _ in mpl.__version__.split('.'))[:2] < (3, 6):
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

        self._update_transScale()

    def _set_lim_and_transforms(self):
        super()._set_lim_and_transforms()
        transTernaryScale = TernaryScaleTransform(self.ternary_scale)
        transTLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewTLim, self.transScale))
        transLLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewLLim, self.transScale))
        transRLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewRLim, self.transScale))

        corners_axes = self.corners_axes

        taxis_transform = TernaryTransform(corners_axes, 0)
        laxis_transform = TernaryTransform(corners_axes, 1)
        raxis_transform = TernaryTransform(corners_axes, 2)

        self._taxis_transform = transTLimits + taxis_transform + self.transAxes
        self._laxis_transform = transLLimits + laxis_transform + self.transAxes
        self._raxis_transform = transRLimits + raxis_transform + self.transAxes

        # For axis labels
        t_l_t = TernaryPerpendicularTransform(self.transAxes, corners_axes, 0)
        l_l_t = TernaryPerpendicularTransform(self.transAxes, corners_axes, 1)
        r_l_t = TernaryPerpendicularTransform(self.transAxes, corners_axes, 2)
        self._taxis_label_transform = t_l_t
        self._laxis_label_transform = l_l_t
        self._raxis_label_transform = r_l_t

        # From ternary coordinates to the original data coordinates
        self.transProjection = (transTernaryScale
                                + BarycentricTransform(self.corners_data))

        # From ternary coordinates to the original Axes coordinates
        self._ternary_axes_transform = self.transProjection + self.transLimits

        # From barycentric coordinates to the original Axes coordinates
        self.transAxesProjection = BarycentricTransform(self.corners_axes)

        # From barycentric coordinates to display coordinates
        self.transTernaryAxes = self.transAxesProjection + self.transAxes

    def get_xaxis_transform(self, which='grid'):
        # Overridden not to call spines
        return self._xaxis_transform

    def get_yaxis_transform(self, which='grid'):
        # Overridden not to call spines
        return self._yaxis_transform

    def get_taxis_transform(self, which='grid'):
        if which == 'label':
            return self._taxis_label_transform
        else:
            return self._taxis_transform

    def get_laxis_transform(self, which='grid'):
        if which == 'label':
            return self._laxis_label_transform
        else:
            return self._laxis_transform

    def get_raxis_transform(self, which='grid'):
        if which == 'label':
            return self._raxis_label_transform
        else:
            return self._raxis_transform

    def _get_axis_text_transform(self, pad_points, trans, indices):
        pad_shift = TernaryShift(indices, self.figure, self.axes, pad_points)
        # `va` and `ha` are modified in `TernaryTick`
        return trans + pad_shift, 'top', 'center'

    def get_taxis_text1_transform(self, pad_points):
        trans = self.get_taxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, [1, 2])

    def get_taxis_text2_transform(self, pad_points):
        trans = self.get_taxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, [2, 1])

    def get_laxis_text1_transform(self, pad_points):
        trans = self.get_laxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, [2, 0])

    def get_laxis_text2_transform(self, pad_points):
        trans = self.get_laxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, [0, 2])

    def get_raxis_text1_transform(self, pad_points):
        trans = self.get_raxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, [0, 1])

    def get_raxis_text2_transform(self, pad_points):
        trans = self.get_raxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, [1, 0])

    def _gen_axes_patch(self):
        return mpatches.Polygon(self.corners_axes)

    def _gen_axes_spines(self, locations=None, offset=0.0, units='inches'):
        # Use `Spine` in `mpltern`
        return {side: Spine.linear_spine(self, side)
                for side in ['tside', 'lside', 'rside']}

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
        self.set_tlim(0.0, self.ternary_scale)
        self.set_llim(0.0, self.ternary_scale)
        self.set_rlim(0.0, self.ternary_scale)
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

    def _create_bbox_from_ternary_lim(self):
        scale = self.ternary_scale
        tmin = self.get_tlim()[0]
        lmin = self.get_llim()[0]
        rmin = self.get_rlim()[0]
        points = [
            [scale - lmin - rmin, lmin, rmin],
            [tmin, scale - tmin - rmin, rmin],
            [tmin, lmin, scale - tmin - lmin],
        ]
        points = self.transProjection.transform(points)
        bbox = mtransforms.Bbox.unit()
        bbox.update_from_data_xy(points, ignore=True)
        return bbox

    def set_ternary_lim(self, tmin, tmax, lmin, lmax, rmin, rmax):
        """

        Notes
        -----
        xmin, xmax : holizontal limits of the triangle
        ymin, ymax : bottom and top of the triangle
        """
        boxin = self._create_bbox_from_ternary_lim()

        scale = self.ternary_scale

        self.set_tlim(tmin, scale - lmin - rmin)
        self.set_llim(lmin, scale - tmin - rmin)
        self.set_rlim(rmin, scale - tmin - lmin)

        boxout = self._create_bbox_from_ternary_lim()

        trans = mtransforms.BboxTransform(boxin, boxout)

        xmin, xmax = self.get_xlim()
        ymin, ymax = self.get_ylim()
        points = [[xmin, ymin], [xmax, ymax]]
        ((xmin, ymin), (xmax, ymax)) = trans.transform(points)

        self.set_xlim(xmin, xmax)
        self.set_ylim(ymin, ymax)

    def set_ternary_min(self, tmin, lmin, rmin):
        scale = self.ternary_scale
        tmax = scale - lmin - rmin
        lmax = scale - rmin - tmin
        rmax = scale - tmin - lmin
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax)

    def set_ternary_max(self, tmax, lmax, rmax):
        scale = self.ternary_scale
        tmin = (scale + tmax - lmax - rmax) * 0.5
        lmin = (scale + lmax - rmax - tmax) * 0.5
        rmin = (scale + rmax - tmax - lmax) * 0.5
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax)

    def get_tlim(self):
        return tuple(self.viewTLim.intervalx)

    def get_llim(self):
        return tuple(self.viewLLim.intervalx)

    def get_rlim(self):
        return tuple(self.viewRLim.intervalx)

    def set_tlim(self, tmin, tmax):
        self.viewTLim.intervalx = (tmin, tmax)
        self.stale = True
        return tmin, tmax

    def set_llim(self, lmin, lmax):
        self.viewLLim.intervalx = (lmin, lmax)
        self.stale = True
        return lmin, lmax

    def set_rlim(self, rmin, rmax):
        self.viewRLim.intervalx = (rmin, rmax)
        self.stale = True
        return rmin, rmax

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
        points = trans.transform(self.corners_axes)

        tmax = points[0, 0]
        tmin = points[1, 0]
        lmax = points[1, 1]
        lmin = points[2, 1]
        rmax = points[2, 2]
        rmin = points[0, 2]

        self.set_tlim(tmin, tmax)
        self.set_llim(lmin, lmax)
        self.set_rlim(rmin, rmax)
