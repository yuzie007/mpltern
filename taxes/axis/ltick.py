import numpy as np

from .ternary_tick import TernaryTick


class LTick(TernaryTick):
    def _get_text1_transform(self):
        return self.axes.get_laxis_text1_transform(self._pad)

    def _get_text2_transform(self):
        return self.axes.get_laxis_text1_transform(self._pad)

    def _get_tick1line(self):
        l = super()._get_tick1line()
        l.set_transform(self.axes.get_laxis_transform(which='tick1'))
        return l

    def _get_tick2line(self):
        l = super()._get_tick2line()
        l.set_transform(self.axes.get_laxis_transform(which='tick2'))
        return l

    def _get_gridline(self):
        l = super()._get_gridline()
        l.set_transform(self.axes.get_laxis_transform(which='grid'))
        return l

    def update_position(self, loc):
        super().update_position(loc)
        # angle = np.deg2rad(210)
        ps = self.axes.transAxes.transform([[0.0, 0.0], [-0.5, -1.0]])
        angle = np.arctan2(ps[1, 0] - ps[0, 0], ps[1, 1] - ps[0, 1])
        self.tilt(self.tick1line, angle)
        self.tilt(self.tick2line, angle + np.pi)
