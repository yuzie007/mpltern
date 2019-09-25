import numpy as np

from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
from matplotlib.axis import XAxis
from .ltick import LTick


class LAxis(XAxis):
    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        return LTick(self.axes, 0, '', major=major, **tick_kw)

    def _get_label(self):
        # x in axes coords, y in display coords (to be updated at draw
        # time by _update_label_positions)
        label = mtext.Text(x=0.5, y=0.0,
                           fontproperties=font_manager.FontProperties(
                               size=rcParams['axes.labelsize'],
                               weight=rcParams['axes.labelweight']),
                           color=rcParams['axes.labelcolor'],
                           verticalalignment='bottom',
                           horizontalalignment='center',
                           rotation=60,
                           rotation_mode='anchor')
        label.set_transform(self.axes._vertical_laxis_transform)

        self._set_artist_props(label)
        self.label_position = 'bottom'
        return label

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

        pad = self.labelpad * self.figure.dpi / 72

        x, y = self.label.get_position()
        if self.label_position == 'bottom':
            trans = self.axes._vertical_laxis_transform
            points = []
            for bbox in bboxes:
                points.extend([
                    [bbox.x0, bbox.y0],
                    [bbox.x0, bbox.y1],
                    [bbox.x1, bbox.y0],
                    [bbox.x1, bbox.y1],
                ])
            # In case bboxes do not exists, spines are used.
            points.extend(trans.transform(((0.0, 0.0), (1.0, 0.0))))
            points = trans.inverted().transform(points)
            y = min(points[:, 1])
            position = (x, y - pad)
            self.label.set_position(position)
            self.label.set_transform(trans)

        elif self.label_position == 'top':
            trans = self.axes._vertical_baxis_transform
            points = []
            for bbox in bboxes2:
                points.extend([
                    [bbox.x0, bbox.y0],
                    [bbox.x0, bbox.y1],
                    [bbox.x1, bbox.y0],
                    [bbox.x1, bbox.y1],
                ])
            # In case bboxes do not exists, spines are used.
            points.extend(trans.transform(((0.0, 0.0), (1.0, 0.0))))
            points = trans.inverted().transform(points)
            y = min(points[:, 1])
            position = (x, y - pad)
            self.label.set_position(position)
            self.label.set_transform(trans)

        else:  # "corner"
            baxis = self.axes.baxis
            raxis = self.axes.raxis
            laxis = self.axes.laxis
            bbboxes, bbboxes2 = baxis._get_tick_boxes_siblings(renderer=renderer)
            rbboxes, rbboxes2 = raxis._get_tick_boxes_siblings(renderer=renderer)
            lbboxes, lbboxes2 = laxis._get_tick_boxes_siblings(renderer=renderer)
            bbox = mtransforms.Bbox.union(
                bbboxes + bbboxes2 + rbboxes + rbboxes2 + lbboxes + lbboxes2)
            dx = ((self.axes.bbox.x0 - bbox.x0) + (bbox.x1 - self.axes.bbox.x1)) * 0.5
            x = self.axes.bbox.x0 - dx
            position = (x, bbox.y0 - pad)
            self.label.set_position(position)
            self.label.set_transform(mtransforms.IdentityTransform())

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

        points = ((xmin, 0.0), (xmax, 0.0), (xmin, 1.0))
        ps = trans.transform(points)

        if self.label_position == 'bottom':
            d0 = ps[1] - ps[0]
        elif self.label_position == 'top':
            d0 = ps[2] - ps[1]
        else:
            d0 = ps[0] - ps[2]

        angle = np.arctan2(d0[1], d0[0])
        angle = np.rad2deg(angle)  # [-180, +180]

        # For readability, the angle is adjusted to be in [-90, +90]
        label_rotation = (angle + 90.0) % 180.0 - 90.0

        d0 = ps[1] - ps[0]
        d1 = ps[2] - ps[1]
        d = d0[0] * d1[1] - d1[0] * d0[1]
        clockwise = (d < 0.0)  # For the triangle
        is_corner = self.label_position not in ['bottom', 'top']
        if clockwise:
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
