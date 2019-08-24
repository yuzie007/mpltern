import matplotlib.transforms as mtransforms
from matplotlib.axis import XTick


class TernaryTick(XTick):
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
