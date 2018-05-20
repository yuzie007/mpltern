from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from matplotlib.artist import allow_rasterization
from matplotlib import rcParams
import matplotlib.lines as mlines
from matplotlib.axis import XTick, GRIDLINE_INTERPOLATION_STEPS


class TernaryTick(XTick):
    def __init__(self, taxes, loc, label, *args, **kwargs):
        self.taxes = taxes
        axes = self.taxes.get_axes()
        super(TernaryTick, self).__init__(axes, loc, label, *args, **kwargs)

    @allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            self.stale = False
            return

        renderer.open_group(self.__name__)
        if self.gridOn:
            self.gridline.draw(renderer)
        if self.tick1On:
            self.tick1line.draw(renderer)
        # if self.tick2On:
        #     self.tick2line.draw(renderer)

        if self.label1On:
            self.label1.draw(renderer)
        # if self.label2On:
        #     self.label2.draw(renderer)
        renderer.close_group(self.__name__)

        self.stale = False

    def _get_tick1line(self):
        'Get the default line2D instance'
        # both x and y in data coords
        scale = {'in': 2, 'inout': 1, 'out': 2}[self._tickdir]
        l = mlines.Line2D(xdata=(0,), ydata=(0,), color=self._color,
                          linestyle='None', marker=self._tickmarkers[0],
                          markersize=self._size * scale,
                          markeredgewidth=self._width, zorder=self._zorder)
        # l.set_transform(self.axes.get_xaxis_transform(which='tick1'))
        l.set_transform(self.axes.transData)
        self._set_artist_props(l)
        return l

    def _get_tick2line(self):
        'Get the default line2D instance'
        # both x and y in data coords
        scale = {'in': 2, 'inout': 1, 'out': 2}[self._tickdir]
        l = mlines.Line2D(xdata=(0,), ydata=(1,),
                          color=self._color,
                          linestyle='None',
                          marker=self._tickmarkers[1],
                          markersize=self._size * scale,
                          markeredgewidth=self._width, zorder=self._zorder)
        # l.set_transform(self.axes.get_xaxis_transform(which='tick2'))
        l.set_transform(self.axes.transData)
        self._set_artist_props(l)
        return l

    def _get_gridline(self):
        'Get the default line2D instance'
        # both x and y in data coords
        l = mlines.Line2D(xdata=(0.0, 0.0), ydata=(0, 1.0),
                          color=rcParams['grid.color'],
                          linestyle=rcParams['grid.linestyle'],
                          linewidth=rcParams['grid.linewidth'],
                          alpha=rcParams['grid.alpha'],
                          markersize=0)
        # l.set_transform(self.axes.get_xaxis_transform(which='grid'))
        l.set_transform(self.axes.transData)
        l.get_path()._interpolation_steps = GRIDLINE_INTERPOLATION_STEPS
        self._set_artist_props(l)

        return l
