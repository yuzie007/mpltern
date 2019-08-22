import matplotlib.transforms as mtransforms
from matplotlib.axis import XTick


class TernaryTick(XTick):
    def _get_tick2line(self):
        # Instead of _get_tick2line, _get_tick1line is called to avoid
        # the dependence on spines.
        l = super()._get_tick1line()
        # xdata and ydata must be blank to suppress unexpected lines/points.
        l.set_xdata(())
        l.set_ydata(())
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
