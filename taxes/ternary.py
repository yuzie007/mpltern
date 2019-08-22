from collections import OrderedDict

import numpy as np

from matplotlib import cbook
from matplotlib import docstring
from matplotlib.axes import Axes
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
from .spines import Spine
from .transforms import BAxisTransform, RAxisTransform, LAxisTransform
from .axis.baxis import BAxis
from .axis.raxis import RAxis
from .axis.laxis import LAxis


def brl2xy(b, r, l):
    b = np.asarray(b)
    r = np.asarray(r)
    l = np.asarray(l)
    x = b + 0.5 * r
    y = 0.5 * np.sqrt(3.0) * r
    return x, y


def xy2brl(x, y, s=1.0):
    x = np.asarray(x)
    y = np.asarray(y)
    s = np.asarray(s)
    b = s * (x - y / np.sqrt(3.0))
    r = s * (y / np.sqrt(3.0) * 2.0)
    l = s * (1.0 - x - y / np.sqrt(3.0))
    return b, r, l


class TernaryAxesBase(Axes):
    def __init__(self, *args, scale=1.0, **kwargs):
        self._scale = scale
        super().__init__(*args, **kwargs)
        self.set_aspect('equal', adjustable='box', anchor='C')
        self.set_tlim(0.0, scale, 0.0, scale, 0.0, scale)

    def set_figure(self, fig):
        self.viewBLim = mtransforms.Bbox.unit()
        self.viewRLim = mtransforms.Bbox.unit()
        self.viewLLim = mtransforms.Bbox.unit()
        super().set_figure(fig)

    def _gen_axes_patch(self):
        """
        Returns the patch used to draw the background of the axes.  It
        is also used as the clipping path for any data elements on the
        axes.

        In the standard axes, this is a rectangle, but in other
        projections it may not be.

        .. note::

            Intended to be overridden by new projection types.

        """
        return mpatches.Polygon(((0.0, 0.0), (1.0, 0.0), (0.5, 1.0)))

    def _gen_axes_spines(self, locations=None, offset=0.0, units='inches'):
        """
        Returns a dict whose keys are spine names and values are
        Line2D or Patch instances. Each element is used to draw a
        spine of the axes.

        In the standard axes, this is a single line segment, but in
        other projections it may not be.

        .. note::

            Intended to be overridden by new projection types.

        """
        return OrderedDict((side, Spine.linear_spine(self, side))
                           for side in ['left', 'right', 'bottom'])

    def _get_axis_list(self):
        return (self.baxis, self.raxis, self.laxis)

    def _init_axis(self):
        """Reference: matplotlib/axes/_base.py, _init_axis

        TODO: Manage spines
        """
        self.baxis = BAxis(self)
        self.raxis = RAxis(self)
        self.laxis = LAxis(self)

        self.xaxis = self.baxis  # TODO
        self.yaxis = self.laxis  # TODO

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

        self._baxis_transform = transBLimits + BAxisTransform() + self.transAxes
        self._raxis_transform = transRLimits + RAxisTransform() + self.transAxes
        self._laxis_transform = transLLimits + LAxisTransform() + self.transAxes

    def get_baxis_transform(self, which='grid'):
        return self._baxis_transform

    def get_raxis_transform(self, which='grid'):
        return self._raxis_transform

    def get_laxis_transform(self, which='grid'):
        return self._laxis_transform

    def get_baxis_text1_transform(self, pad_points):
        x = pad_points / 72.0 * -0.5
        y = pad_points / 72.0 * -np.sqrt(3.0) * 0.5
        return (self.get_baxis_transform(which='tick1') +
                mtransforms.ScaledTranslation(x, y,
                                              self.figure.dpi_scale_trans),
                "top", "center")

    def get_raxis_text1_transform(self, pad_points):
        x = pad_points / 72.0
        y = 0
        return (self.get_raxis_transform(which='tick1') +
                mtransforms.ScaledTranslation(x, y,
                                              self.figure.dpi_scale_trans),
                "center_baseline", "left")

    def get_laxis_text1_transform(self, pad_points):
        x = pad_points / 72.0 * -0.5
        y = pad_points / 72.0 * np.sqrt(3.0) * 0.5
        return (self.get_laxis_transform(which='tick1') +
                mtransforms.ScaledTranslation(x, y,
                                              self.figure.dpi_scale_trans),
                "baseline", "right")

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
        self.set_blim(0.0, self._scale)
        self.set_rlim(0.0, self._scale)
        self.set_llim(0.0, self._scale)
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
        s = self._scale
        if (abs(b - s) > 1e-12) or (abs(r - s) > 1e-12) or (abs(l - s) > 1e-12):
            raise ValueError(b, r, l, s)
        ax = self._axes

        xmin = bmin + 0.5 * rmin
        xmax = bmax + 0.5 * rmin
        ax.set_xlim(xmin, xmax, *args, **kwargs)

        ymin = 0.5 * np.sqrt(3.0) * rmin
        ymax = 0.5 * np.sqrt(3.0) * rmax
        ax.set_ylim(ymin, ymax, *args, **kwargs)

        self.set_blim(bmin, bmax)
        self.set_rlim(rmin, rmax)
        self.set_llim(lmin, lmax)

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
        x, y = brl2xy(b, r, l)
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
        x, y = brl2xy(b, r, l)
        return super().plot(x, y, *args, **kwargs)

    def scatter(self, b, r, l, *args, **kwargs):
        x, y = brl2xy(b, r, l)
        return super().scatter(x, y, *args, **kwargs)

    def hexbin(self, b, r, l, *args, **kwargs):
        x, y = brl2xy(b, r, l)
        return super().hexbin(x, y, *args, **kwargs)

    def quiver(self, b, r, l, db, dr, dl, *args, **kwargs):
        x, y = brl2xy(b, r, l)
        u, v = brl2xy(b + db, r + dr, l + dl)
        u -= x
        v -= y
        return super().quiver(x, y, u, v, *args, **kwargs)

    def fill(self, b, r, l, *args, **kwargs):
        x, y = brl2xy(b, r, l)
        return super().fill(x, y, *args, **kwargs)

    def tricontour(self, b, r, l, *args, **kwargs):
        x, y = brl2xy(b, r, l)
        return super().tricontour(x, y, *args, **kwargs)

    def tricontourf(self, b, r, l, *args, **kwargs):
        x, y = brl2xy(b, r, l)
        return super().tricontourf(x, y, *args, **kwargs)

    def tripcolor(self, b, r, l, *args, **kwargs):
        x, y = brl2xy(b, r, l)
        return super().tripcolor(x, y, *args, **kwargs)

    def triplot(self, b, r, l, *args, **kwargs):
        x, y = brl2xy(b, r, l)
        tplot = self.plot
        self.plot = super().plot
        tmp = super().triplot(x, y, *args, **kwargs)
        self.plot = tplot
        return tmp
