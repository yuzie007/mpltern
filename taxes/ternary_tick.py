import numpy as np

import matplotlib.transforms as mtransforms
from matplotlib.axis import XTick


class TernaryTick(XTick):
    def _get_text1_transform(self):
        return {
            'ttick': self.axes.get_taxis_text1_transform,
            'ltick': self.axes.get_laxis_text1_transform,
            'rtick': self.axes.get_raxis_text1_transform,
        }[self.tick_name](self._pad)

    def _get_text2_transform(self):
        return {
            'ttick': self.axes.get_taxis_text2_transform,
            'ltick': self.axes.get_laxis_text2_transform,
            'rtick': self.axes.get_raxis_text2_transform,
        }[self.tick_name](self._pad)

    def _get_axis_transform(self, which):
        """Helper method in `taxes` to select an appropriate transform."""
        return {
            'ttick': self.axes.get_taxis_transform,
            'ltick': self.axes.get_laxis_transform,
            'rtick': self.axes.get_raxis_transform,
        }[self.tick_name](which=which)

    def _get_tick1line(self):
        l = super()._get_tick1line()
        l.set_transform(self._get_axis_transform(which='tick1'))
        return l

    def _get_tick2line(self):
        l = super()._get_tick2line()
        l.set_transform(self._get_axis_transform(which='tick2'))
        return l

    def _get_gridline(self):
        l = super()._get_gridline()
        l.set_transform(self._get_axis_transform(which='grid'))
        return l

    def update_position(self, loc):
        super().update_position(loc)
        # The angle here is given for the "in" ticks.
        trans = self._get_axis_transform(which='grid')
        ps = trans.transform([[0.0, 0.0], [0.0, 1.0]])
        angle = np.arctan2(ps[1, 1] - ps[0, 1], ps[1, 0] - ps[0, 0])
        self.tilt(self.tick1line, angle - np.pi / 2)
        self.tilt(self.tick2line, angle + np.pi / 2)

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


class TTick(TernaryTick):
    tick_name = 'ttick'


class LTick(TernaryTick):
    tick_name = 'ltick'


class RTick(TernaryTick):
    tick_name = 'rtick'


