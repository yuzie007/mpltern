from collections import OrderedDict

import numpy as np

from matplotlib import cbook, rcParams
from matplotlib.cbook import (
    _OrderedSet, _check_1d, iterable, index_of, get_label)
from matplotlib import docstring
from matplotlib.axes import Axes
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.tri as mtri
from .spines import Spine
from matplotlib.tri import Triangulation
from .axis.baxis import BAxis
from .axis.raxis import RAxis
from .axis.laxis import LAxis

__author__ = 'Yuji Ikeda'


def abc2xy(a, b, c):
    x = a + 0.5 * b
    y = 0.5 * np.sqrt(3.0) * b
    return x, y


def xy2abc(x, y, s=1.0):
    a = s * (x - y / np.sqrt(3.0))
    b = s * (y / np.sqrt(3.0) * 2.0)
    c = s * (1.0 - x - y / np.sqrt(3.0))
    return a, b, c


class TernaryAxesBase(Axes):
    def __init__(self, *args, scale=1.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_aspect('equal', adjustable='box', anchor='C')
        self._scale = scale
        self.set_tlim(0.0, scale, 0.0, scale, 0.0, scale)

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

    def get_axes(self):
        return self._axes

    def _get_axis_list(self):
        return (self.baxis, self.raxis, self.laxis)

    def _init_axis(self):
        """Reference: matplotlib/axes/_base.py, _init_axis

        TODO: Manage spines
        """
        self.baxis = BAxis(self)
        self.xaxis = self.baxis
        self.raxis = RAxis(self)
        self.yaxis = self.raxis
        self.laxis = LAxis(self)

        self.spines['bottom'].register_axis(self.baxis)
        self.spines['right'].register_axis(self.raxis)
        self.spines['left'].register_axis(self.laxis)

        self._update_transScale()

    # def get_baxis_text1_transform(self, pad_points):
    #     return (self._ax.transData +
    #             mtransforms.ScaledTranslation(0, -1 * pad_points / 72.0,
    #                                           self.figure.dpi_scale_trans),
    #             "top", "center")

    def get_baxis_text1_transform(self, pad_points):
        return (self._axes.transData +
                mtransforms.ScaledTranslation(-0.5 * pad_points / 72.0, -np.sqrt(3.0) * 0.5 * pad_points / 72.0,
                                              self.figure.dpi_scale_trans),
                "top", "center")

    def get_raxis_text1_transform(self, pad_points):
        return (self._axes.transData +
                mtransforms.ScaledTranslation(1 * pad_points / 72.0, 0,
                                              self.figure.dpi_scale_trans),
                "center_baseline", "left")

    def get_laxis_text1_transform(self, pad_points):
        return (self._axes.transData +
                mtransforms.ScaledTranslation(-0.5 * pad_points / 72.0, np.sqrt(3.0) * 0.5 * pad_points / 72.0,
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

    def get_children(self):
        """return a list of child artists"""
        children = []
        children.extend(self.collections)
        children.extend(self.patches)
        children.extend(self.lines)
        children.extend(self.texts)
        children.extend(self.artists)
        children.extend(self.spines.values())
        children.append(self.baxis)
        children.append(self.raxis)
        children.append(self.laxis)
        children.append(self.title)
        children.append(self._left_title)
        children.append(self._right_title)
        children.extend(self.tables)
        children.extend(self.images)
        children.extend(self.child_axes)

        if self.legend_ is not None:
            children.append(self.legend_)
        children.append(self.patch)

        return children

    def cla(self):
        self._blim = (0.0, 1.0)
        self._rlim = (0.0, 1.0)
        self._llim = (0.0, 1.0)
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

    def _get_corner_points(self):
        scale = self._scale
        points = [
            [0.0, 0.0],
            [scale, 0.0],
            [0.5 * scale, np.sqrt(3.0) * 0.5 * scale],
            ]
        return np.array(points)

    def set_tlim(self, bmin, bmax, rmin, rmax, lmin, lmax, *args, **kwargs):
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

        self._blim = (bmin, bmax)
        self._rlim = (rmin, rmax)
        self._llim = (lmin, lmax)

    def get_blim(self):
        return self._blim

    def get_rlim(self):
        return self._rlim

    def get_llim(self):
        return self._llim


class TernaryAxes(TernaryAxesBase):
    """
    A ternary graph projection, where the input dimensions are *b*, *r*, *l*.
    The plot starts from the bottom and goes anti-clockwise.
    """
    name = 'ternary'

    def text(self, b, r, l, s, *args, **kwargs):
        x, y = abc2xy(b, r, l)
        return super().text(x, y, s, *args, **kwargs)

    def text_xy(self, x, y, s, *args, **kwargs):
        super().text(x, y, s, *args, **kwargs)

    def plot(self, b, r, l, *args, **kwargs):
        x, y = abc2xy(b, r, l)
        return super().plot(x, y, *args, **kwargs)

    def triplot(self, *args, **kwargs):
        return mtri.triplot(super(), *args, **kwargs)

    def scatter(self, b, r, l, *args, **kwargs):
        x, y = abc2xy(b, r, l)
        return self._axes.scatter(x, y, *args, **kwargs)

    def _create_triangulation(self, a, b, c):
        x, y = abc2xy(a, b, c)
        return Triangulation(x, y)


class TernaryTriangulation(Triangulation):
    def __init__(self, a, b, c, *args, **kwargs):
        x, y = abc2xy(a, b, c)
        super().__init__(x, y, *args, **kwargs)
