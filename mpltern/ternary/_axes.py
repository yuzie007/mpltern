from collections import OrderedDict
import logging

import numpy as np

import matplotlib as mpl
from matplotlib import _api, cbook
from matplotlib.axes import Axes
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.axis as maxis
from mpltern.ternary.spines import Spine
from mpltern.ternary.transforms import (
    TernaryTransform, TernaryPerpendicularTransform,
    BarycentricTransform, TernaryScaleTransform, TernaryShift)
from mpltern.ternary.axis import TAxis, LAxis, RAxis
from mpltern.ternary.ternary_parser import (
    _parse_ternary_single, _parse_ternary_multiple,
    _parse_ternary_vector, _parse_ternary_vector_field)

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
        spines = OrderedDict((side, Spine.linear_spine(self, side))
                             for side in ['tside', 'lside', 'rside'])
        return spines

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

    def grid(self, b=None, which='major', axis='both', **kwargs):
        """
        Configure the grid lines.

        Parameters
        ----------
        b : bool or None, optional
            Whether to show the grid lines. If any *kwargs* are supplied,
            it is assumed you want the grid on and *b* will be set to True.

            If *b* is *None* and there are no *kwargs*, this toggles the
            visibility of the lines.

        which : {'major', 'minor', 'both'}, optional
            The grid lines to apply the changes on.

        axis : {'both', 't', 'l', 'r'}, optional
            The axis to apply the changes on.

        **kwargs : `.Line2D` properties
            Define the line properties of the grid, e.g.::

                grid(color='r', linestyle='-', linewidth=2)

            Valid *kwargs* are

        %(_Line2D_docstr)s

        Notes
        -----
        The axis is drawn as a unit, so the effective zorder for drawing the
        grid is determined by the zorder of each axis, not by the zorder of the
        `.Line2D` objects comprising the grid.  Therefore, to set grid zorder,
        use `.set_axisbelow` or, for more control, call the
        `~matplotlib.axis.Axis.set_zorder` method of each axis.
        """
        if len(kwargs):
            b = True
        _api.check_in_list(['t', 'l', 'r', 'both'], axis=axis)
        if axis in ['t', 'both']:
            self.taxis.grid(b, which=which, **kwargs)
        if axis in ['l', 'both']:
            self.laxis.grid(b, which=which, **kwargs)
        if axis in ['r', 'both']:
            self.raxis.grid(b, which=which, **kwargs)

    def tick_params(self, axis='both', **kwargs):
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

    def _create_bbox_from_ternary_lim(self):
        tmin, tmax = self.get_tlim()
        lmin, lmax = self.get_llim()
        rmin, rmax = self.get_rlim()
        points = [[tmax, lmin, rmin], [tmin, lmax, rmin], [tmin, lmin, rmax]]
        points = self.transProjection.transform(points)
        bbox = mtransforms.Bbox.unit()
        bbox.update_from_data_xy(points, ignore=True)
        return bbox

    def set_ternary_lim(self, tmin, tmax, lmin, lmax, rmin, rmax, *args, **kwargs):
        """

        Notes
        -----
        xmin, xmax : holizontal limits of the triangle
        ymin, ymax : bottom and top of the triangle
        """
        t = tmax + lmin + rmin
        l = tmin + lmax + rmin
        r = tmin + lmin + rmax
        s = self.ternary_scale
        tol = 1e-12
        if (abs(t - s) > tol) or (abs(l - s) > tol) or (abs(r - s) > tol):
            raise ValueError(t, l, r, s)

        boxin = self._create_bbox_from_ternary_lim()

        self.set_tlim(tmin, tmax)
        self.set_llim(lmin, lmax)
        self.set_rlim(rmin, rmax)

        boxout = self._create_bbox_from_ternary_lim()

        trans = mtransforms.BboxTransform(boxin, boxout)

        xmin, xmax = self.get_xlim()
        ymin, ymax = self.get_ylim()
        points = [[xmin, ymin], [xmax, ymax]]
        ((xmin, ymin), (xmax, ymax)) = trans.transform(points)

        self.set_xlim(xmin, xmax)
        self.set_ylim(ymin, ymax)

    def set_ternary_min(self, tmin, lmin, rmin, *args, **kwargs):
        s = self.ternary_scale
        tmax = s - lmin - rmin
        lmax = s - rmin - tmin
        rmax = s - tmin - lmin
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax, *args, **kwargs)

    def set_ternary_max(self, tmax, lmax, rmax, *args, **kwargs):
        s = self.ternary_scale
        tmin = (s + tmax - lmax - rmax) * 0.5
        lmin = (s + lmax - rmax - tmax) * 0.5
        rmin = (s + rmax - tmax - lmax) * 0.5
        self.set_ternary_lim(tmin, tmax, lmin, lmax, rmin, rmax, *args, **kwargs)

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
        Return *True* if this axes supports the zoom box button functionality.

        Ternary axes do not support zoom boxes.
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


class TernaryAxes(TernaryAxesBase):
    """
    A ternary graph projection, where the input dimensions are *t*, *l*, *r*.
    The plot starts from the bottom and goes anti-clockwise.
    """
    name = 'ternary'

    def get_tlabel(self):
        """
        Get the tlabel text string.
        """
        label = self.taxis.get_label()
        return label.get_text()

    def set_tlabel(self, tlabel, fontdict=None, labelpad=None, **kwargs):
        if labelpad is not None:
            self.taxis.labelpad = labelpad
        return self.taxis.set_label_text(tlabel, fontdict, **kwargs)

    def get_llabel(self):
        """
        Get the llabel text string.
        """
        label = self.laxis.get_label()
        return label.get_text()

    def set_llabel(self, llabel, fontdict=None, labelpad=None, **kwargs):
        if labelpad is not None:
            self.laxis.labelpad = labelpad
        return self.laxis.set_label_text(llabel, fontdict, **kwargs)

    def get_rlabel(self):
        """
        Get the rlabel text string.
        """
        label = self.raxis.get_label()
        return label.get_text()

    def set_rlabel(self, rlabel, fontdict=None, labelpad=None, **kwargs):
        if labelpad is not None:
            self.raxis.labelpad = labelpad
        return self.raxis.set_label_text(rlabel, fontdict, **kwargs)

    @_parse_ternary_single
    def text(self, *args, **kwargs):
        return super().text(*args, **kwargs)

    def axtline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a equi-t line across the axes.

        Parameters
        ----------
        x : scalar, optional, default: 0
            x position in data coordinates of the equi-t line.

        ymin : scalar, optional, default: 0
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        ymax : scalar, optional, default: 1
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        Returns
        -------
        line : :class:`~matplotlib.lines.Line2D`

        Other Parameters
        ----------------
        **kwargs
            Valid kwargs are :class:`~matplotlib.lines.Line2D` properties,
            with the exception of 'transform':

        %(_Line2D_docstr)s

        See also
        --------
        axtspan : Add a equi-t span across the axis.
        """
        if "transform" in kwargs:
            raise ValueError(
                "'transform' is not allowed as a kwarg;"
                + "axtline generates its own transform.")
        trans = self.get_taxis_transform(which='grid')
        l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
        self.add_line(l)
        return l

    def axlline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a equi-l line across the axes.

        Parameters
        ----------
        x : scalar, optional, default: 0
            x position in data coordinates of the equi-l line.

        ymin : scalar, optional, default: 0
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        ymax : scalar, optional, default: 1
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        Returns
        -------
        line : :class:`~matplotlib.lines.Line2D`

        Other Parameters
        ----------------
        **kwargs
            Valid kwargs are :class:`~matplotlib.lines.Line2D` properties,
            with the exception of 'transform':

        %(_Line2D_docstr)s

        See also
        --------
        axlspan : Add a equi-l span across the axis.
        """
        if "transform" in kwargs:
            raise ValueError(
                "'transform' is not allowed as a kwarg;"
                + "axlline generates its own transform.")
        trans = self.get_laxis_transform(which='grid')
        l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
        self.add_line(l)
        return l

    def axrline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a equi-r line across the axes.

        Parameters
        ----------
        x : scalar, optional, default: 0
            x position in data coordinates of the equi-r line.

        ymin : scalar, optional, default: 0
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        ymax : scalar, optional, default: 1
            Should be between 0 and 1, 0 being one end of the plot, 1 the
            other of the plot.

        Returns
        -------
        line : :class:`~matplotlib.lines.Line2D`

        Other Parameters
        ----------------
        **kwargs
            Valid kwargs are :class:`~matplotlib.lines.Line2D` properties,
            with the exception of 'transform':

        %(_Line2D_docstr)s

        See also
        --------
        axrspan : Add a equi-r span across the axis.
        """
        if "transform" in kwargs:
            raise ValueError(
                "'transform' is not allowed as a kwarg;"
                + "axrline generates its own transform.")
        trans = self.get_raxis_transform(which='grid')
        l = mlines.Line2D([x, x], [ymin, ymax], transform=trans, **kwargs)
        self.add_line(l)
        return l

    def axline(self, xy1, xy2=None, *, slope=None, **kwargs):
        k = 'transform'
        if k in kwargs and kwargs[k].input_dims == 2:
            return super().axline(xy1, xy2, slope=slope, **kwargs)

        if k in kwargs and kwargs[k] == self.transTernaryAxes:
            trans = self.transAxesProjection
            trans_xy = self.transAxes
        else:
            trans = self.transProjection
            trans_xy = None

        tlr1 = xy1
        tlr2 = xy2

        xy1 = trans.transform(tlr1)
        if xy2 is not None:
            xy2 = trans.transform(tlr2)
        if slope is not None:
            slope = np.asarray(slope)
            if slope.size != 3:
                raise ValueError("'slope' must be of length 3")
            xy3 = trans.transform(tlr1 + np.asarray(slope))
            dx = xy3[0] - xy1[0]
            dy = xy3[1] - xy1[1]
            if np.allclose(dx, 0.0):
                slope = np.inf
            else:
                slope = dy / dx

        if k in kwargs:
            kwargs['transform'] = trans_xy

        return super().axline(xy1, xy2, slope=slope, **kwargs)

    def axtspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        """
        Add a span for the bottom coordinate.

        Parameters
        ----------
        xmin : float
               Lower limit of the top span in data units.
        xmax : float
               Upper limit of the top span in data units.
        ymin : float, optional, default: 0
               Lower limit of the span from end to end in relative
               (0-1) units.
        ymax : float, optional, default: 1
               Upper limit of the span from end to end in relative
               (0-1) units.

        Returns
        -------
        Polygon : `~matplotlib.patches.Polygon`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Polygon` properties.

        %(Polygon)s

        See Also
        --------
        axlspan : Add a span for the left coordinate.
        axrspan : Add a span for the right coordinate.
        """
        trans = self.get_taxis_transform(which='grid')
        verts = (xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)
        p = mpatches.Polygon(verts, **kwargs)
        p.set_transform(trans)
        self.add_patch(p)
        return p

    def axlspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        """
        Add a span for the left coordinate.

        Parameters
        ----------
        xmin : float
               Lower limit of the left span in data units.
        xmax : float
               Upper limit of the left span in data units.
        ymin : float, optional, default: 0
               Lower limit of the span from end to end in relative
               (0-1) units.
        ymax : float, optional, default: 1
               Upper limit of the span from end to end in relative
               (0-1) units.

        Returns
        -------
        Polygon : `~matplotlib.patches.Polygon`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Polygon` properties.

        %(Polygon)s

        See Also
        --------
        axbspan : Add a span for the bottom coordinate.
        axrspan : Add a span for the right coordinate.
        """
        trans = self.get_laxis_transform(which='grid')
        verts = (xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)
        p = mpatches.Polygon(verts, **kwargs)
        p.set_transform(trans)
        self.add_patch(p)
        return p

    def axrspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        """
        Add a span for the right coordinate.

        Parameters
        ----------
        xmin : float
               Lower limit of the right span in data units.
        xmax : float
               Upper limit of the right span in data units.
        ymin : float, optional, default: 0
               Lower limit of the span from end to end in relative
               (0-1) units.
        ymax : float, optional, default: 1
               Upper limit of the span from end to end in relative
               (0-1) units.

        Returns
        -------
        Polygon : `~matplotlib.patches.Polygon`

        Other Parameters
        ----------------
        **kwargs : `~matplotlib.patches.Polygon` properties.

        %(Polygon)s

        See Also
        --------
        axbspan : Add a span for the bottom coordinate.
        axlspan : Add a span for the left coordinate.
        """
        trans = self.get_raxis_transform(which='grid')
        verts = (xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)
        p = mpatches.Polygon(verts, **kwargs)
        p.set_transform(trans)
        self.add_patch(p)
        return p

    @_parse_ternary_multiple
    def plot(self, *args, **kwargs):
        return super().plot(*args, **kwargs)

    @_parse_ternary_multiple
    def scatter(self, *args, **kwargs):
        return super().scatter(*args, **kwargs)

    @_parse_ternary_single
    def hexbin(self, *args, **kwargs):
        return super().hexbin(*args, **kwargs)

    @_parse_ternary_vector
    def arrow(self, *args, **kwargs):
        return super().arrow(*args, **kwargs)

    @_parse_ternary_vector_field
    def quiver(self, *args, **kwargs):
        return super().quiver(*args, **kwargs)

    @_parse_ternary_multiple
    def fill(self, *args, **kwargs):
        return super().fill(*args, **kwargs)

    @_parse_ternary_single
    def hist2d(self, *args, **kwargs):
        return super().hist2d(*args, **kwargs)

    @_parse_ternary_single
    def tricontour(self, *args, **kwargs):
        return super().tricontour(*args, **kwargs)

    @_parse_ternary_single
    def tricontourf(self, *args, **kwargs):
        return super().tricontourf(*args, **kwargs)

    @_parse_ternary_single
    def tripcolor(self, *args, **kwargs):
        return super().tripcolor(*args, **kwargs)

    @_parse_ternary_single
    def triplot(self, *args, **kwargs):
        return super().triplot(*args, **kwargs)
