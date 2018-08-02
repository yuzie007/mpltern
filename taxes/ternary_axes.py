from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from collections import OrderedDict

import six

from operator import attrgetter

import numpy as np

import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.artist as martist
import matplotlib.image as mimage
from matplotlib.axes import Axes
from .spines import Spine
from matplotlib.tri import Triangulation
from .axis.baxis import BAxis
from .axis.raxis import RAxis
from .axis.laxis import LAxis

from matplotlib import rcParams

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


# class TernaryAxesBase(object):
class TernaryAxesBase(martist.Artist):
    def __init__(self, ax, scale,
                 facecolor=None,
                 frameon=True):
        super(TernaryAxesBase, self).__init__()
        self._axes = ax
        self.figure = ax.get_figure()
        self._scale = scale

        if facecolor is None:
            facecolor = rcParams['axes.facecolor']
        self._facecolor = facecolor
        self._frameon = frameon
        self._axisbelow = rcParams['axes.axisbelow']

        self.cla()

        self.spines = self._gen_axes_spines()
        # for s in six.itervalues(self.spines):
        #     self._axes.add_artist(s)

        self._init_axis()

        self._axes.add_artist(self)

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
        # points = self._get_corner_points()
        return mpatches.Polygon(((0.0, 0.0), (1.0, 0.0), (0.5, 1.0)), zorder=0)
        # return mpatches.Rectangle((0.0, 0.0), 1.0, 1.0)

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
        return OrderedDict([
            ('left', Spine.linear_spine(self._axes, 'left')),
            ('right', Spine.linear_spine(self._axes, 'right')),
            ('bottom', Spine.linear_spine(self._axes, 'bottom'))])
        # return OrderedDict([
        #     ('left', Spine.linear_spine(self._axes, 'left', clip_on=False)),
        #     ('right', Spine.linear_spine(self._axes, 'right', clip_on=False)),
        #     ('bottom', Spine.linear_spine(self._axes, 'bottom', clip_on=False))])

    def set_facecolor(self, color):
        self._facecolor = color
        return self.patch.set_facecolor(color)
    set_fc = set_facecolor

    def get_axes(self):
        return self._axes

    def _init_axis(self):
        """Reference: matplotlib/axes/_base.py, _init_axis

        TODO: Manage spines
        """
        self.baxis = BAxis(self)
        self.raxis = RAxis(self)
        self.laxis = LAxis(self)

        self.spines['bottom'].register_axis(self.baxis)
        self.spines['right'].register_axis(self.raxis)
        self.spines['left'].register_axis(self.laxis)

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
        children = []
        children.append(self.baxis)
        children.append(self.raxis)
        children.append(self.laxis)
        children.extend(six.itervalues(self.spines))
        children.append(self.patch)
        return children

    def draw(self, renderer, inframe=False):
        artists = self.get_children()

        if self.axison and not inframe:
            if self._axisbelow is True:
                self.baxis.set_zorder(0.5)
                self.raxis.set_zorder(0.5)
                self.laxis.set_zorder(0.5)
            elif self._axisbelow is False:
                self.baxis.set_zorder(2.5)
                self.raxis.set_zorder(2.5)
                self.laxis.set_zorder(2.5)
            else:
                # 'line': above patches, below lines
                self.baxis.set_zorder(1.5)
                self.raxis.set_zorder(1.5)
                self.laxis.set_zorder(1.5)
        else:
            for _axis in self._get_axis_list():
                artists.remove(_axis)

        artists = sorted(artists, key=attrgetter('zorder'))

        mimage._draw_list_compositing_images(renderer, self, artists)
        # super(TernaryAxesBase, self).draw(renderer, *args, **kwargs)

    def _get_corner_points(self):
        scale = self._scale
        points = [
            [0.0, 0.0],
            [scale, 0.0],
            [0.5 * scale, np.sqrt(3.0) * 0.5 * scale],
            ]
        return np.array(points)

    def set_axis_on(self):
        return Axes.set_axis_on(self)

    def cla(self):
        self._blim = (0.0, 1.0)
        self._rlim = (0.0, 1.0)
        self._llim = (0.0, 1.0)

        # The patch draws the background of the axes.  We want this to be below
        # the other artists.  We use the frame to draw the edges so we are
        # setting the edgecolor to None.
        self.patch = self._gen_axes_patch()
        self.patch.set_figure(self.figure)
        self.patch.set_facecolor(self._facecolor)
        self.patch.set_edgecolor('None')
        self.patch.set_linewidth(0)
        self.patch.set_transform(self._axes.transAxes)

        self.set_axis_on()

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

    def __init__(self, *args, **kwargs):
        super(TernaryAxes, self).__init__(*args, **kwargs)
        self._init_axes()

    def _init_axes(self):
        ax = self._axes
        scale = self._scale

        ax.axis('off')
        ax.axis('scaled')

        self.set_tlim(0.0, scale, 0.0, scale, 0.0, scale)

    def plot(self, a, b, c, *args, **kwargs):
        x, y = abc2xy(a, b, c)
        self._axes.plot(x, y, *args, **kwargs)

    def _create_triangulation(self, a, b, c):
        x, y = abc2xy(a, b, c)
        return Triangulation(x, y)


class TernaryTriangulation(Triangulation):
    def __init__(self, a, b, c, *args, **kwargs):
        x, y = abc2xy(a, b, c)
        super().__init__(x, y, *args, **kwargs)
