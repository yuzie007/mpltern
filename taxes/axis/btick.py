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
        xmax = self.axes.get_xlim()[-1]
        if self.tick1On:
            self.tick1line.set_xdata((loc,))
        if self.tick2On:
            self.tick2line.set_xdata((loc,))
        if self.gridOn:
            self.gridline.set_xdata((loc, loc + (xmax - loc) * 0.5))
            self.gridline.set_ydata((0, (xmax - loc) * np.sqrt(3.0) * 0.5))
        if self.label1On:
            self.label1.set_x(loc)
        if self.label2On:
            self.label2.set_x(loc)

        self._loc = loc
        self.stale = True
