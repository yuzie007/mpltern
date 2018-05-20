from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
from .ternary_axis import TernaryAxis
from .rtick import RTick


class RAxis(TernaryAxis):
    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        return RTick(self.taxes, 0, '', major=major, **tick_kw)

    def _get_label(self):
        # x in axes coords, y in display coords (to be updated at draw
        # time by _update_label_positions)
        label = mtext.Text(x=0.75, y=0.5,
                           fontproperties=font_manager.FontProperties(
                               size=rcParams['axes.labelsize'],
                               weight=rcParams['axes.labelweight']),
                           color=rcParams['axes.labelcolor'],
                           verticalalignment='bottom_baseline',
                           horizontalalignment='center',
                           rotation=-60,
                           rotation_mode='anchor')
        label.set_transform(mtransforms.blended_transform_factory(
            mtransforms.IdentityTransform(), self.axes.transAxes))

        self._set_artist_props(label)
        self.label_position = 'bottom'
        return label

    def _update_label_position(self, bboxes, bboxes2):
        """
        Update the label position based on the bounding box enclosing
        all the ticklabels and axis spine
        """
        if not self._autolabelpos:
            return
        x, y = self.label.get_position()
        if True:
            try:
                spine = self.axes.spines['right']
                spinebbox = spine.get_transform().transform_path(
                    spine.get_path()).get_extents()
            except KeyError:
                # use axes if spine doesn't exist
                spinebbox = self.axes.bbox

            def extract_right(bbox):
                bbox_axes = bbox.transformed(self.axes.transAxes.inverted())
                x = bbox_axes.x1 + (bbox_axes.y1 - y) * 0.5
                return self.axes.transAxes.transform((x, y))[0]

            right = min([extract_right(bbox) for bbox in bboxes])

            self.label.set_position(
                (right + self.labelpad * self.figure.dpi / 72.0, y)
            )
