import numpy as np

from matplotlib.axis import XAxis
from matplotlib import rcParams
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
from taxes.ternary_tick import TTick, LTick, RTick


class TernaryAxis(XAxis):
    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        return {
            't': TTick,
            'l': LTick,
            'r': RTick,
        }[self.axis_name](self.axes, 0, '', major=major, **tick_kw)

    def _get_label(self):
        """

        Notes
        -----
        x : data coordinates in the axis direction
        y : display (pixel) coordinates in the direction vertical to the
            axis direction, updated when drawn in `_update_label_positions`
        """
        self.label_position = 'corner'
        label = mtext.Text(x=0.5, y=0.0,
                           fontproperties=font_manager.FontProperties(
                               size=rcParams['axes.labelsize'],
                               weight=rcParams['axes.labelweight']),
                           color=rcParams['axes.labelcolor'],
                           verticalalignment='top',
                           horizontalalignment='center',
                           rotation=0,
                           rotation_mode='anchor')
        trans = {
            't': self.axes._vertical_taxis_transform,
            'l': self.axes._vertical_laxis_transform,
            'r': self.axes._vertical_raxis_transform,
        }[self.axis_name]
        label.set_transform(trans)

        self._set_artist_props(label)
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

        Called from `get_tightbbox` and `draw`.
        """
        if not self._autolabelpos:
            return

        pad = self.labelpad * self.figure.dpi / 72

        if self.label_position == 'bottom':
            trans = {
                't': self.axes._vertical_laxis_transform,
                'l': self.axes._vertical_raxis_transform,
                'r': self.axes._vertical_taxis_transform,
            }[self.axis_name]
            lim = max if self.axes.clockwise else min
            x = 0.5
        elif self.label_position == 'top':
            trans = {
                't': self.axes._vertical_raxis_transform,
                'l': self.axes._vertical_taxis_transform,
                'r': self.axes._vertical_laxis_transform,
            }[self.axis_name]
            lim = max if self.axes.clockwise else min
            x = 0.5
        else:  # "corner"
            trans = {
                't': self.axes._vertical_taxis_transform,
                'l': self.axes._vertical_laxis_transform,
                'r': self.axes._vertical_raxis_transform,
            }[self.axis_name]

            # Get the corner in the display coordinates, and then get
            # the *x* coordinates in the `trans` coordinates
            corner_index = {'t': 0, 'l': 1, 'r': 2}[self.axis_name]
            corners = self.axes.transAxes.transform(self.axes.corners)
            corner = corners[corner_index]
            x = trans.inverted().transform(corner)[0]

            lim = min if self.axes.clockwise else max

        scale = 1.0 if lim == max else -1.0

        points = self._get_points(renderer=renderer)
        points = trans.inverted().transform(points)
        y = lim(points[:, 1])
        position = (x, y + scale * pad)

        self.label.set_position(position)
        self.label.set_transform(trans)
        angle, va = self._get_label_rotation()
        self.label.set_verticalalignment(va)
        self.label.set_rotation(angle)
        self.label.set_rotation_mode('anchor')

    def get_view_interval(self):
        'return the Interval instance for this axis view limits'
        return {
            't': self.axes.get_tlim,
            'l': self.axes.get_llim,
            'r': self.axes.get_rlim,
        }[self.axis_name]()

    def _get_points(self, renderer):
        """Get the points of all tick labels in the pixel coordinates."""
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

    def _get_label_rotation(self):
        """Determine the axis-label rotation and alignment.

        Returns
        -------
        label_rotation : float
            Rotation of the axis label in degree.
        va : str
            Vertical alignment of the axis label as a parameter of `Text`.
        """
        # Corners in the pixel coordinates
        corners = self.axes.transAxes.transform(self.axes.corners)

        # Index of the corner
        index = {'t': 0, 'l': 1, 'r': 2}[self.axis_name]
        if self.label_position == 'bottom':
            c0, c1, c2 = np.roll(corners,  1 - index, axis=0)
        elif self.label_position == 'top':
            c0, c1, c2 = np.roll(corners,  0 - index, axis=0)
        else:  # elif self.xy == 'corner':
            c0, c1, c2 = np.roll(corners, -1 - index, axis=0)

        d = c1 - c0
        axis_angle = np.rad2deg(np.arctan2(d[1], d[0]))  # [-180, +180]

        is_corner_label = (self.label_position not in ['bottom', 'top'])

        # `label_rotation` and `va` are determined by comparing the coordinates
        # of the midpoint of the axis with those of the other corner point.
        midpoint = (c0 + c1) * 0.5
        tol = 1e-6
        if abs(abs(axis_angle) - 90.0) < tol:  # axis_angle is -90 or 90.
            # (the other corner is on the right side) xor
            # (the label is at the other corner)
            if (c2[0] > midpoint[0]) ^ is_corner_label:
                label_rotation = 90.0
            else:
                label_rotation = -90.0
            va = 'bottom'  # Because the label faces to the axis.
        else:
            # For readability, the angle is adjusted to be in [-90, +90]
            label_rotation = (axis_angle + 90.0) % 180.0 - 90.0
            # (the other corner is below the axis) xor
            # (the label is at the other corner)
            if (c2[1] < midpoint[1]) ^ is_corner_label:
                va = 'bottom'
            else:
                va = 'top'

        return label_rotation, va


class TAxis(TernaryAxis):
    axis_name = 't'


class LAxis(TernaryAxis):
    axis_name = 'l'


class RAxis(TernaryAxis):
    axis_name = 'r'
