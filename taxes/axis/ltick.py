from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np

from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
from .ternary_tick import TernaryTick


class LTick(TernaryTick):
    def _get_text1_transform(self):
        return self.taxes.get_laxis_text1_transform(self._pad)

    def _get_text2_transform(self):
        return self.taxes.get_laxis_text1_transform(self._pad)

    def _get_text1(self):
        'This may be overridden when rotating tick labels'
        return super(TernaryTick, self)._get_text1()

    def update_position(self, loc):
        'Set the location of tick in data coords with scalar *loc*'
        xmin, xmax = self.axes.get_xlim()
        ymin, ymax = self.axes.get_ylim()
        xavg = (xmin + xmax) * 0.5

        lmin, lmax = self.taxes.get_llim()

        sx0 = (xmin - xavg) / (lmax - lmin)
        sx1 = (xmin - xmax) / (lmax - lmin)
        sy1 = (ymin - ymax) / (lmax - lmin)

        locx0 = xavg + sx0 * (loc - lmin)
        locx1 = xmax + sx1 * (loc - lmin)
        locy0 = ymax + sy1 * (loc - lmin)
        locy1 = ymin

        angle = np.deg2rad(210)

        if self.tick1On:
            self.tick1line.set_xdata((locx0,))
            self.tick1line.set_ydata((locy0,))
            self.tilt(self.tick1line, angle)
        if self.tick2On:
            self.tick2line.set_xdata((locx0,))
            self.tick2line.set_ydata((locy0,))
            self.tilt(self.tick2line, angle)
        if self.gridOn:
            self.gridline.set_xdata((locx0, locx1))
            self.gridline.set_ydata((locy0, locy1))
        if self.label1On:
            self.label1.set_x(locx0)
            self.label1.set_y(locy0)
        if self.label2On:
            self.label2.set_x(locx0)
            self.label2.set_y(locy0)

        self._loc = loc
        self.stale = True
