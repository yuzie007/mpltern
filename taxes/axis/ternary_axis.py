import numpy as np

from matplotlib.axis import XAxis


class TernaryAxis(XAxis):
    def set_label_position(self, position):
        """
        Set the label position (edge or corner)

        Parameters
        ----------
        position : {'edge', 'corner'}
        """
        self.label_position = position
        self.stale = True

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

    def _get_points(self, renderer):
        points = []
        taxis = self.axes.taxis
        laxis = self.axes.laxis
        raxis = self.axes.raxis
        tbboxes, tbboxes2 = taxis._get_tick_boxes_siblings(renderer=renderer)
        lbboxes, lbboxes2 = laxis._get_tick_boxes_siblings(renderer=renderer)
        rbboxes, rbboxes2 = raxis._get_tick_boxes_siblings(renderer=renderer)
        bboxes = tbboxes + tbboxes2 + lbboxes + lbboxes2 + rbboxes + rbboxes2
        for bbox in bboxes:
            points.extend([
                [bbox.x0, bbox.y0],
                [bbox.x0, bbox.y1],
                [bbox.x1, bbox.y0],
                [bbox.x1, bbox.y1],
            ])
        # In case bboxes do not exists, spines are used.
        points.extend(self.axes.transAxes.transform(self.axes.corners))
        return np.asarray(points)
