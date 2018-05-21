from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np

from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
from .ternary_tick import TernaryTick


class BTick(TernaryTick):
    def _get_text1_transform(self):
        return self.taxes.get_baxis_text1_transform(self._pad)

    def _get_text2_transform(self):
        return self.taxes.get_baxis_text1_transform(self._pad)

    def apply_tickdir(self, tickdir):
        if tickdir is None:
            tickdir = rcParams['%s.direction' % self._name]
        self._tickdir = tickdir

        if self._tickdir == 'in':
            self._tickmarkers = ((1, 2, 330), (1, 2, 150))
        elif self._tickdir == 'inout':
            self._tickmarkers = ((2, 2, 330), (2, 2, 330))
        else:
            self._tickmarkers = ((1, 2, 150), (1, 2, 330))
        self._pad = self._base_pad + self.get_tick_padding()
        self.stale = True

    def _get_text1(self):
        'This may be overridden when rotating tick labels'
        return super(TernaryTick, self)._get_text1()

    def update_position(self, loc):
        xmin, xmax = self.axes.get_xlim()
        ymin, ymax = self.axes.get_ylim()
        locx1 = loc + (xmax - loc) * 0.5
        a = (ymax - ymin) / (xmax - xmin)
        locy1 = ymin + a * (xmax - loc)

        if self.tick1On:
            self.tick1line.set_xdata((loc,))
            self.tick1line.set_ydata((ymin,))
        if self.tick2On:
            self.tick2line.set_xdata((loc,))
            self.tick2line.set_ydata((ymin,))
        if self.gridOn:
            self.gridline.set_xdata((loc, locx1))
            self.gridline.set_ydata((ymin, locy1))
        if self.label1On:
            self.label1.set_x(loc)
            self.label1.set_y(ymin)
        if self.label2On:
            self.label2.set_x(loc)
            self.label2.set_y(ymin)

        self._loc = loc
        self.stale = True
