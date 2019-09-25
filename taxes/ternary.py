from collections import OrderedDict

import numpy as np

from matplotlib import cbook
from matplotlib import docstring
from matplotlib.axes import Axes
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.axis as maxis
from .spines import Spine
from .transforms import (
    TernaryTransform, VerticalTernaryTransform, TernaryDataTransform)
from .axis.baxis import BAxis
from .axis.raxis import RAxis
from .axis.laxis import LAxis


def xy2brl(x, y, s=1.0):
    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    b = s * (x - y / np.sqrt(3.0))
    r = s * (y / np.sqrt(3.0) * 2.0)
    l = s * (1.0 - x - y / np.sqrt(3.0))
    return b, r, l


def _determine_anchor(angle0, angle1):
    """Determine the tick-label alignments from the spine and the tick angles.

    Parameters
    ----------
    angle0 : float
        Spine angle in radian.
    angle1 : float
        Tick angle in radian.

    Returns
    -------
    ha : str
        Horizontal alignment.
    va : str
        Vertical alignment.
    """
    if angle0 < 0.0:
        a0 = angle0 + 180.0
    else:
        a0 = angle0

    if a0 < 30.0:
        if angle1 < a0:
            return 'center', 'top'
        else:
            return 'center', 'bottom'
    elif 30.0 <= a0 < 150.0:
        if angle1 < a0 - 180.0:
            return 'right', 'center_baseline'
        elif a0 - 180.0 <= angle1 < 30.0:
            return 'left', 'center_baseline'
        elif 30.0 <= angle1 < a0:
            return 'left', 'baseline'
        elif a0 <= angle1 < 150.0:
            return 'right', 'baseline'
        else:
            return 'right', 'center_baseline'
    elif 150.0 <= a0:
        if angle1 < a0 - 180.0 or a0 <= angle1:
            return 'center', 'top'
        else:
            return 'center', 'bottom'


class TernaryAxesBase(Axes):
    def __init__(self, *args, scale=1.0, points=None, **kwargs):
        if points is None:
            corners = ((0.0, 0.0), (1.0, 0.0), (0.5, 1.0))
        else:
            corners = points

        self.corners = np.asarray(corners)

        self.scale = scale
        super().__init__(*args, **kwargs)
        self.set_aspect('equal', adjustable='box', anchor='C')
        self.set_tlim(0.0, scale, 0.0, scale, 0.0, scale)

    @property
    def clockwise(self):
        corners = self.transAxes.transform(self.corners)
        d0 = corners[1] - corners[0]
        d1 = corners[2] - corners[1]
        d = d0[0] * d1[1] - d1[0] * d0[1]
        return d < 0.0

    def set_figure(self, fig):
        self.viewBLim = mtransforms.Bbox.unit()
        self.viewRLim = mtransforms.Bbox.unit()
        self.viewLLim = mtransforms.Bbox.unit()
        super().set_figure(fig)

    def _get_axis_list(self):
        return (self.baxis, self.raxis, self.laxis)

    def _init_axis(self):
        self.xaxis = maxis.XAxis(self)
        self.yaxis = maxis.YAxis(self)

        self.baxis = BAxis(self)
        self.raxis = RAxis(self)
        self.laxis = LAxis(self)

        self.spines['bottom'].register_axis(self.baxis)
        self.spines['right'].register_axis(self.raxis)
        self.spines['left'].register_axis(self.laxis)

        self._update_transScale()

    def _set_lim_and_transforms(self):
        super()._set_lim_and_transforms()
        transBLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewBLim, self.transScale))
        transRLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewRLim, self.transScale))
        transLLimits = mtransforms.BboxTransformFrom(
            mtransforms.TransformedBbox(self.viewLLim, self.transScale))

        baxis_transform = TernaryTransform(self.corners, 0)
        raxis_transform = TernaryTransform(self.corners, 1)
        laxis_transform = TernaryTransform(self.corners, 2)

        self._baxis_transform = transBLimits + baxis_transform + self.transAxes
        self._raxis_transform = transRLimits + raxis_transform + self.transAxes
        self._laxis_transform = transLLimits + laxis_transform + self.transAxes

        # For axis labels
        self._vertical_baxis_transform = VerticalTernaryTransform(self.transAxes, self.corners, 0)
        self._vertical_raxis_transform = VerticalTernaryTransform(self.transAxes, self.corners, 1)
        self._vertical_laxis_transform = VerticalTernaryTransform(self.transAxes, self.corners, 2)

        # For data
        self._ternary_data_transform = TernaryDataTransform(
            self.transLimits, self.scale, self.corners)

    def get_baxis_transform(self, which='grid'):
        return self._baxis_transform

    def get_raxis_transform(self, which='grid'):
        return self._raxis_transform

    def get_laxis_transform(self, which='grid'):
        return self._laxis_transform

    def _get_axis_text_transform(self, pad_points, trans, which):
        if which == 'tick1':
            ps0 = trans.transform([[0.0, 0.0], [1.0, 0.0]])
            ps1 = trans.transform([[0.0, 0.0], [0.0, 1.0]])
        else:
            ps0 = trans.transform([[0.0, 1.0], [1.0, 1.0]])
            ps1 = trans.transform([[0.0, 1.0], [0.0, 0.0]])
        d0 = ps0[0] - ps0[1]
        d1 = ps1[0] - ps1[1]
        angle0 = np.rad2deg(np.arctan2(d0[1], d0[0]))
        angle1 = np.rad2deg(np.arctan2(d1[1], d1[0]))
        ha, va = _determine_anchor(angle0, angle1)
        x, y = d1 / np.linalg.norm(d1) * pad_points / 72.0
        return (trans +
                mtransforms.ScaledTranslation(x, y,
                                              self.figure.dpi_scale_trans),
                va, ha)

    def get_baxis_text1_transform(self, pad_points):
        trans = self.get_baxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, 'tick1')

    def get_baxis_text2_transform(self, pad_points):
        trans = self.get_baxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, 'tick2')

    def get_raxis_text1_transform(self, pad_points):
        trans = self.get_raxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, 'tick1')

    def get_raxis_text2_transform(self, pad_points):
        trans = self.get_raxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, 'tick2')

    def get_laxis_text1_transform(self, pad_points):
        trans = self.get_laxis_transform(which='tick1')
        return self._get_axis_text_transform(pad_points, trans, 'tick1')

    def get_laxis_text2_transform(self, pad_points):
        trans = self.get_laxis_transform(which='tick2')
        return self._get_axis_text_transform(pad_points, trans, 'tick2')

    def _gen_axes_patch(self):
        return mpatches.Polygon(self.corners)
    _gen_axes_patch.__doc__ = Axes._gen_axes_patch.__doc__

    def _gen_axes_spines(self, locations=None, offset=0.0, units='inches'):
        return OrderedDict((side, Spine.linear_spine(self, side))
                           for side in ['left', 'right', 'bottom', 'top'])
    _gen_axes_spines.__doc__ = Axes._gen_axes_spines.__doc__

    def get_baxis(self):
        """Return the BAxis instance"""
        return self.baxis

    def get_raxis(self):
        """Return the RAxis instance"""
        return self.raxis

    def get_laxis(self):
        """Return the LAxis instance"""
        return self.laxis

    def cla(self):
        self.set_blim(0.0, self.scale)
        self.set_rlim(0.0, self.scale)
        self.set_llim(0.0, self.scale)
        super().cla()

    @docstring.dedent_interpd
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

        axis : {'both', 'b', 'r', 'l'}, optional
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
        cbook._check_in_list(['b', 'r', 'l', 'both'], axis=axis)
        if axis in ['b', 'both']:
            self.baxis.grid(b, which=which, **kwargs)
        if axis in ['r', 'both']:
            self.raxis.grid(b, which=which, **kwargs)
        if axis in ['l', 'both']:
            self.laxis.grid(b, which=which, **kwargs)

    def tick_params(self, axis='both', **kwargs):
        cbook._check_in_list(['b', 'r', 'l', 'both'], axis=axis)
        if axis in ['b', 'both']:
            bkw = dict(kwargs)
            bkw.pop('left', None)
            bkw.pop('right', None)
            bkw.pop('labelleft', None)
            bkw.pop('labelright', None)
            self.baxis.set_tick_params(**bkw)
        if axis in ['r', 'both']:
            rkw = dict(kwargs)
            rkw.pop('left', None)
            rkw.pop('right', None)
            rkw.pop('labelleft', None)
            rkw.pop('labelright', None)
            self.raxis.set_tick_params(**rkw)
        if axis in ['l', 'both']:
            lkw = dict(kwargs)
            lkw.pop('left', None)
            lkw.pop('right', None)
            lkw.pop('labelleft', None)
            lkw.pop('labelright', None)
            self.laxis.set_tick_params(**lkw)

    def set_tlim(self, bmin, bmax, rmin, rmax, lmin, lmax, *args, **kwargs):
        """

        Notes
        -----
        xmin, xmax : holizontal limits of the triangle
        ymin, ymax : bottom and top of the triangle
        """
        b = bmax + rmin + lmin
        r = bmin + rmax + lmin
        l = bmin + rmin + lmax
        s = self.scale
        tol = 1e-12
        if (abs(b - s) > tol) or (abs(r - s) > tol) or (abs(l - s) > tol):
            raise ValueError(b, r, l, s)

        self.set_blim(bmin, bmax)
        self.set_rlim(rmin, rmax)
        self.set_llim(lmin, lmax)

        xmin = bmin + 0.5 * rmin
        xmax = bmax + 0.5 * rmin
        self.set_xlim(xmin, xmax, *args, **kwargs)

        ymin = 0.5 * np.sqrt(3.0) * rmin
        ymax = 0.5 * np.sqrt(3.0) * rmax
        self.set_ylim(ymin, ymax, *args, **kwargs)

    def get_blim(self):
        return tuple(self.viewBLim.intervalx)

    def get_rlim(self):
        return tuple(self.viewRLim.intervalx)

    def get_llim(self):
        return tuple(self.viewLLim.intervalx)

    def set_blim(self, bmin, bmax):
        self.viewBLim.intervalx = (bmin, bmax)
        self.stale = True
        return bmin, bmax

    def set_rlim(self, rmin, rmax):
        self.viewRLim.intervalx = (rmin, rmax)
        self.stale = True
        return rmin, rmax

    def set_llim(self, lmin, lmax):
        self.viewLLim.intervalx = (lmin, lmax)
        self.stale = True
        return lmin, lmax

    def opposite_ticks(self, b=None):
        if b:
            self.baxis.set_label_position('top')
            self.raxis.set_label_position('top')
            self.laxis.set_label_position('top')
            self.baxis.set_ticks_position('top')
            self.raxis.set_ticks_position('top')
            self.laxis.set_ticks_position('top')
        else:
            self.baxis.set_label_position('bottom')
            self.raxis.set_label_position('bottom')
            self.laxis.set_label_position('bottom')
            self.baxis.set_ticks_position('bottom')
            self.raxis.set_ticks_position('bottom')
            self.laxis.set_ticks_position('bottom')


class TernaryAxes(TernaryAxesBase):
    """
    A ternary graph projection, where the input dimensions are *b*, *r*, *l*.
    The plot starts from the bottom and goes anti-clockwise.
    """
    name = 'ternary'

    def get_blabel(self):
        """
        Get the blabel text string.
        """
        label = self.baxis.get_label()
        return label.get_text()

    def set_blabel(self, blabel, fontdict=None, labelpad=None, **kwargs):
        if labelpad is not None:
            self.baxis.labelpad = labelpad
        return self.baxis.set_label_text(blabel, fontdict, **kwargs)

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

    def text(self, b, r, l, s, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        return super().text(x, y, s, *args, **kwargs)

    def text_xy(self, x, y, s, *args, **kwargs):
        return super().text(x, y, s, *args, **kwargs)

    def axbline(self, x=0, ymin=0, ymax=1, **kwargs):
        """
        Add a equi-b line across the axes.

        Parameters
        ----------
        x : scalar, optional, default: 0
            x position in data coordinates of the equi-b line.

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
        axbspan : Add a equi-b span across the axis.
        """
        if "transform" in kwargs:
            raise ValueError(
                "'transform' is not allowed as a kwarg;"
                + "axbline generates its own transform.")
        trans = self.get_baxis_transform(which='grid')
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

    def axbspan(self, xmin, xmax, ymin=0, ymax=1, **kwargs):
        """
        Add a span for the bottom coordinate.

        Parameters
        ----------
        xmin : float
               Lower limit of the bottom span in data units.
        xmax : float
               Upper limit of the bottom span in data units.
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
        axrspan : Add a span for the right coordinate.
        axlspan : Add a span for the left coordinate.
        """
        trans = self.get_baxis_transform(which='grid')
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

    def plot(self, b, r, l, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        return super().plot(x, y, *args, **kwargs)

    def scatter(self, b, r, l, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        return super().scatter(x, y, *args, **kwargs)

    def hexbin(self, b, r, l, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        return super().hexbin(x, y, *args, **kwargs)

    def quiver(self, b, r, l, db, dr, dl, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        brl = np.column_stack((b + db, r + dr, l + dl))
        u, v = self._ternary_data_transform.transform(brl).T
        u -= x
        v -= y
        return super().quiver(x, y, u, v, *args, **kwargs)

    def fill(self, b, r, l, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        return super().fill(x, y, *args, **kwargs)

    def tricontour(self, b, r, l, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        return super().tricontour(x, y, *args, **kwargs)

    def tricontourf(self, b, r, l, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        return super().tricontourf(x, y, *args, **kwargs)

    def tripcolor(self, b, r, l, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        return super().tripcolor(x, y, *args, **kwargs)

    def triplot(self, b, r, l, *args, **kwargs):
        brl = np.column_stack((b, r, l))
        x, y = self._ternary_data_transform.transform(brl).T
        tplot = self.plot
        self.plot = super().plot
        tmp = super().triplot(x, y, *args, **kwargs)
        self.plot = tplot
        return tmp
