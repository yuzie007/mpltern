from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
from .ternary_axis import TernaryAxis
from .btick import BTick


class BAxis(TernaryAxis):
    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        return BTick(self.taxes, 0, '', major=major, **tick_kw)

    def _get_label(self):
        # x in axes coords, y in display coords (to be updated at draw
        # time by _update_label_positions)
        label = mtext.Text(x=0.5, y=0,
                           fontproperties=font_manager.FontProperties(
                               size=rcParams['axes.labelsize'],
                               weight=rcParams['axes.labelweight']),
                           color=rcParams['axes.labelcolor'],
                           verticalalignment='top',
                           horizontalalignment='center')

        label.set_transform(mtransforms.blended_transform_factory(
            self.axes.transAxes, mtransforms.IdentityTransform()))

        self._set_artist_props(label)
        self.label_position = 'bottom'
        return label

    def _get_tick_boxes_siblings(self, renderer):
        """
        Get the bounding boxes for this `.axis` and its siblings
        as set by `.Figure.align_xlabels` or  `.Figure.align_ylablels`.

        By default it just gets bboxes for self.
        """
        bboxes = []
        bboxes2 = []
        # get the Grouper that keeps track of x-label groups for this figure
        grp = self.figure._align_xlabel_grp
        # if we want to align labels from other axes:
        ticks_to_draw = self._update_ticks()
        tlb, tlb2 = self._get_tick_bboxes(ticks_to_draw, renderer)
        bboxes.extend(tlb)
        bboxes2.extend(tlb2)
        return bboxes, bboxes2

    def _update_label_position(self, renderer):
        """
        Update the label position based on the bounding box enclosing
        all the ticklabels and axis spine
        """
        if not self._autolabelpos:
            return

        # get bounding boxes for this axis and any siblings
        # that have been set by `fig.align_xlabels()`
        bboxes, bboxes2 = self._get_tick_boxes_siblings(renderer=renderer)

        x, y = self.label.get_position()
        if self.label_position == 'bottom':
            try:
                spine = self.axes.spines['bottom']
                spinebbox = spine.get_transform().transform_path(
                    spine.get_path()).get_extents()
            except KeyError:
                # use axes if spine doesn't exist
                spinebbox = self.axes.bbox
            bbox = mtransforms.Bbox.union(bboxes + [spinebbox])
            bottom = bbox.y0

            self.label.set_position(
                (x, bottom - self.labelpad * self.figure.dpi / 72)
            )

    def get_view_interval(self):
        'return the Interval instance for this axis view limits'
        return self.taxes.get_blim()
