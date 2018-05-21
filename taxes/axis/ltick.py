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

    def apply_tickdir(self, tickdir):
        if tickdir is None:
            tickdir = rcParams['%s.direction' % self._name]
        self._tickdir = tickdir

        if self._tickdir == 'in':
            self._tickmarkers = ((1, 2, 210), (1, 2, 30))
        elif self._tickdir == 'inout':
            self._tickmarkers = ((2, 2, 210), (2, 2, 210))
        else:
            self._tickmarkers = ((1, 2, 30), (1, 2, 210))
        self._pad = self._base_pad + self.get_tick_padding()
        self.stale = True

    def _get_text1(self):
        'This may be overridden when rotating tick labels'
        return super(TernaryTick, self)._get_text1()

    def update_position(self, loc):
        'Set the location of tick in data coords with scalar *loc*'
        xmin, xmax = self.axes.get_xlim()
        ymin, ymax = self.axes.get_ylim()
        locx0 = xmin + (xmax - loc) * 0.5
        locx1 = xmin + (xmax - loc)
        a = (ymax - ymin) / (xmax - xmin)
        locy0 = ymin + a * (xmax - loc)

        if self.tick1On:
            self.tick1line.set_xdata((locx0,))
            self.tick1line.set_ydata((locy0,))
        if self.tick2On:
            self.tick2line.set_xdata((locx0,))
            self.tick2line.set_ydata((locy0,))
        if self.gridOn:
            self.gridline.set_xdata((locx0, locx1))
            self.gridline.set_ydata((locy0, ymin))
        if self.label1On:
            self.label1.set_x(locx0)
            self.label1.set_y(locy0)
        if self.label2On:
            self.label2.set_x(locx0)
            self.label2.set_y(locy0)

        self._loc = loc
        self.stale = True
