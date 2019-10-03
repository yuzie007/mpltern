import numpy as np

from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
from .ternary_axis import TernaryAxis
from .ltick import LTick


class LAxis(TernaryAxis):
    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        return LTick(self.axes, 0, '', major=major, **tick_kw)

    def _get_label(self):
        """

        Notes
        -----
        x : data coordinates in the axis direction
        y : display (pixel) coordinates in the direction vertical to the
            axis direction, updated when drawn in `_update_label_positions`
        """
        self.label_position = 'corner'
        rotation, va = self._get_label_rotation()
        label = mtext.Text(x=0.5, y=0.0,
                           fontproperties=font_manager.FontProperties(
                               size=rcParams['axes.labelsize'],
                               weight=rcParams['axes.labelweight']),
                           color=rcParams['axes.labelcolor'],
                           verticalalignment=va,
                           horizontalalignment='center',
                           rotation=rotation,
                           rotation_mode='anchor')
        label.set_transform(self.axes._vertical_laxis_transform)

        self._set_artist_props(label)
        return label

    def _update_label_position(self, renderer):
        """
        Update the label position based on the bounding box enclosing
        all the ticklabels and axis spine
        """
        if not self._autolabelpos:
            return

        pad = self.labelpad * self.figure.dpi / 72

        if self.label_position == 'bottom':
            trans = self.axes._vertical_raxis_transform
            lim = max if self.axes.clockwise else min
        elif self.label_position == 'top':
            trans = self.axes._vertical_taxis_transform
            lim = max if self.axes.clockwise else min
        else:  # "corner"
            trans = self.axes._vertical_laxis_transform
            lim = min if self.axes.clockwise else max

        scale = 1.0 if lim == max else -1.0

        points = self._get_points(renderer=renderer)
        points = trans.inverted().transform(points)
        y = lim(points[:, 1])
        position = (0.5, y + scale * pad)

        self.label.set_position(position)
        self.label.set_transform(trans)
        angle, va = self._get_label_rotation()
        self.label.set_verticalalignment(va)
        self.label.set_rotation(angle)
        self.label.set_rotation_mode('anchor')

    def get_view_interval(self):
        'return the Interval instance for this axis view limits'
        return self.axes.get_llim()

    def _get_label_rotation(self):
        trans = self.axes._laxis_transform
        xmin, xmax = self.axes.get_llim()

        points = ((xmax, 0.0), (xmin, 1.0), (xmin, 0.0))
        ps = trans.transform(points)

        if self.label_position == 'bottom':
            d0 = ps[0] - ps[2]
        elif self.label_position == 'top':
            d0 = ps[1] - ps[0]
        else:
            d0 = ps[2] - ps[1]

        angle = np.arctan2(d0[1], d0[0])
        angle = np.rad2deg(angle)  # [-180, +180]

        # For readability, the angle is adjusted to be in [-90, +90]
        label_rotation = (angle + 90.0) % 180.0 - 90.0

        is_corner = self.label_position not in ['bottom', 'top']
        if self.axes.clockwise:
            if abs(angle) > 90.0:
                if is_corner:
                    va = 'bottom'
                else:
                    va = 'top'
            else:
                if is_corner:
                    va = 'top'
                else:
                    va = 'bottom'
        else:
            if abs(angle) > 90.0:
                if is_corner:
                    va = 'top'
                else:
                    va = 'bottom'
            else:
                if is_corner:
                    va = 'bottom'
                else:
                    va = 'top'

        return label_rotation, va
