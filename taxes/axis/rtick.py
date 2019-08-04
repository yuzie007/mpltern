import numpy as np

from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
from .ternary_tick import TernaryTick


class RTick(TernaryTick):
    def _get_text1_transform(self):
        return self.taxes.get_raxis_text1_transform(self._pad)

    def _get_text2_transform(self):
        return self.taxes.get_raxis_text1_transform(self._pad)

    def _get_text1(self):
        'This may be overridden when rotating tick labels'
        return super(TernaryTick, self)._get_text1()

    def update_position(self, loc):
        'Set the location of tick in data coords with scalar *loc*'
        xmin, xmax = self.axes.get_xlim()
        ymin, ymax = self.axes.get_ylim()
        xavg = (xmin + xmax) * 0.5

        rmin, rmax = self.taxes.get_rlim()

        sx0 = (xavg - xmax) / (rmax - rmin)
        sx1 = (xavg - xmin) / (rmax - rmin)
        sy0 = (ymax - ymin) / (rmax - rmin)

        locx0 = xmax + sx0 * (loc - rmin)
        locx1 = xmin + sx1 * (loc - rmin)
        locy0 = ymin + sy0 * (loc - rmin)
        locy1 = locy0

        angle = np.deg2rad(90)

        self.tick1line.set_xdata((locx0,))
        self.tick1line.set_ydata((locy0,))
        self.tilt(self.tick1line, angle)

        self.tick2line.set_xdata((locx0,))
        self.tick2line.set_ydata((locy0,))
        self.tilt(self.tick2line, angle)

        self.gridline.set_xdata((locx0, locx1))
        self.gridline.set_ydata((locy0, locy1))

        self.label1.set_x(locx0)
        self.label1.set_y(locy0)

        self.label2.set_x(locx0)
        self.label2.set_y(locy0)

        self._loc = loc
        self.stale = True
