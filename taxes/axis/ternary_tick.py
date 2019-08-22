from matplotlib.artist import allow_rasterization
import matplotlib.transforms as mtransforms
from matplotlib.axis import XTick


class TernaryTick(XTick):
    @allow_rasterization
    def draw(self, renderer):
        if not self.get_visible():
            self.stale = False
            return
        renderer.open_group(self.__name__)
        for artist in [self.gridline, self.tick1line, self.tick2line,
                       self.label1, self.label2]:
            artist.draw(renderer)
        renderer.close_group(self.__name__)
        self.stale = False

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
