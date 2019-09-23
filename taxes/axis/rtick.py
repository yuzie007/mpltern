import numpy as np

from .ternary_tick import TernaryTick


class RTick(TernaryTick):
    def _get_text1_transform(self):
        return self.axes.get_raxis_text1_transform(self._pad)

    def _get_text2_transform(self):
        return self.axes.get_raxis_text2_transform(self._pad)

    def _get_tick1line(self):
        l = super()._get_tick1line()
        l.set_transform(self.axes.get_raxis_transform(which='tick1'))
        return l

    def _get_tick2line(self):
        l = super()._get_tick2line()
        l.set_transform(self.axes.get_raxis_transform(which='tick2'))
        return l

    def _get_gridline(self):
        l = super()._get_gridline()
        l.set_transform(self.axes.get_raxis_transform(which='grid'))
        return l

    def update_position(self, loc):
        super().update_position(loc)
        # The angle here is given for the "in" ticks.
        trans = self.axes.get_raxis_transform(which='grid')
        ps = trans.transform([[0.0, 0.0], [0.0, 1.0]])
        angle = np.arctan2(ps[1, 1] - ps[0, 1], ps[1, 0] - ps[0, 0])
        self.tilt(self.tick1line, angle - np.pi / 2)
        self.tilt(self.tick2line, angle + np.pi / 2)
