from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from matplotlib.artist import allow_rasterization
from matplotlib import rcParams
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms
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
        l = super(TernaryTick, self)._get_tick1line()
        l.set_transform(self.axes.transData)
        return l

    def _get_tick2line(self):
        'Get the default line2D instance'
        # both x and y in data coords
        l = super(TernaryTick, self)._get_tick2line()
        l.set_transform(self.axes.transData)
        return l

    def _get_gridline(self):
        'Get the default line2D instance'
        # both x and y in data coords
        l = super(TernaryTick, self)._get_gridline()
        l.set_transform(self.axes.transData)
        return l

    def tilt(self, line, angle):
        if self._tickdir == 'in':
            trans = mtransforms.Affine2D().scale(1.0).rotate(angle)
        elif self._tickdir == 'inout':
            trans = mtransforms.Affine2D().scale(0.5).rotate(angle)
        elif self._tickdir == 'out':
            trans = mtransforms.Affine2D().scale(-1.0).rotate(angle)
        else:
            # Don't modify custom tick line markers.
            trans = line._marker._transform
        line._marker._transform = trans
