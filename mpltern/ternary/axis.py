import numpy as np

from matplotlib.axis import XAxis
from matplotlib import rcParams
import matplotlib.cbook as cbook
import matplotlib.font_manager as font_manager
import matplotlib.text as mtext
from mpltern.ternary.tick import TTick, LTick, RTick


class TernaryAxis(XAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._label_rotation_mode = 'axis'

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
            't': self.axes.get_taxis_transform(which='label'),
            'l': self.axes.get_laxis_transform(which='label'),
            'r': self.axes.get_raxis_transform(which='label'),
        }[self.axis_name]
        label.set_transform(trans)

        self._set_artist_props(label)
        return label

    def set_label_position(self, position):
        """
        Set the label position (corner, tick1, or tick2)

        Parameters
        ----------
        position : {'corner', 'tick1', 'tick2'}
        """
        cbook._check_in_list(['corner', 'tick1', 'tick2'], position=position)
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

        if self.label_position == 'tick1':
            trans = {
                't': self.axes.get_laxis_transform(which='label'),
                'l': self.axes.get_raxis_transform(which='label'),
                'r': self.axes.get_taxis_transform(which='label'),
            }[self.axis_name]
            sign = -1.0  # outward triangle
            x = 0.5  # midpoint of the axis
        elif self.label_position == 'tick2':
            trans = {
                't': self.axes.get_raxis_transform(which='label'),
                'l': self.axes.get_taxis_transform(which='label'),
                'r': self.axes.get_laxis_transform(which='label'),
            }[self.axis_name]
            sign = -1.0  # outward triangle
            x = 0.5  # midpoint of the axis
        else:  # self.label_position == 'corner'
            trans = {
                't': self.axes.get_taxis_transform(which='label'),
                'l': self.axes.get_laxis_transform(which='label'),
                'r': self.axes.get_raxis_transform(which='label'),
            }[self.axis_name]
            sign = 1.0  # inward triangle
            # Get the corner in the display coordinates, and then get
            # the *x* coordinates in the `trans` coordinates
            corner_index = {'t': 0, 'l': 1, 'r': 2}[self.axis_name]
            corners = self.axes.transAxes.transform(self.axes.corners)
            corner = corners[corner_index]
            x = trans.inverted().transform(corner)[0]

        points = self._get_points_surrounding_triangle(renderer=renderer)
        points = trans.inverted().transform(points)
        y = max(sign * points[:, 1]) * sign
        position = (x, y + sign * pad)

        self.label.set_position(position)
        self.label.set_transform(trans)
        angle, ha, va = self._get_label_rotation()
        self.label.set_ha(ha)
        self.label.set_va(va)
        self.label.set_rotation(angle)

    def set_ticks_position(self, position):
        """
        Set the ticks position (tick1, tick2, both, default or none)
        'both' sets the ticks to appear on both positions, but does not
        change the tick labels.
        'none' can be used if you don't want any ticks.
        'none' and 'both' affect only the ticks, not the labels.

        Parameters
        ----------
        position : {'tick1', 'tick2', 'both', 'default', 'none'}
        """
        if position in ['tick1', 'default']:
            self.set_tick_params(which='both', tick1On=True, label1On=True,
                                 tich2On=False, label2On=False)
        elif position == 'tick2':
            self.set_tick_params(which='both', tick1On=False, label1On=False,
                                 tick2On=True, label2On=True)
        elif position == 'both':
            self.set_tick_params(which='both', tick1On=True,
                                 tick2On=True)
        elif position == 'none':
            self.set_tick_params(which='both', tick1On=False,
                                 tick2On=False)
        else:
            raise ValueError("invalid position: %s" % position)
        self.stale = True

    def get_view_interval(self):
        'return the Interval instance for this axis view limits'
        return {
            't': self.axes.get_tlim,
            'l': self.axes.get_llim,
            'r': self.axes.get_rlim,
        }[self.axis_name]()

    # Helper methods for `mpltern`

    def _get_points_surrounding_triangle(self, renderer):
        """Get the points of all tick labels in the pixel coordinates."""
        bboxes_all = []
        for axis in self.axes._get_axis_list():
            bboxes, bboxes2 = axis._get_tick_boxes_siblings(renderer=renderer)
            bboxes_all.extend(bboxes)
            bboxes_all.extend(bboxes2)
        points = []
        for bbox in bboxes_all:
            points.extend([
                [bbox.x0, bbox.y0],
                [bbox.x0, bbox.y1],
                [bbox.x1, bbox.y0],
                [bbox.x1, bbox.y1],
            ])
        # In case no tick labels exist, points of triangle corners are added.
        points.extend(self.axes.transAxes.transform(self.axes.corners))
        return np.asarray(points)

    def set_label_rotation_mode(self, mode):
        """
        Set the mode how to rotate and align the axis-label.

        Parameters
        ----------
        mode : {'axis', 'bottom', 'none'}
        """
        cbook._check_in_list(['axis', 'bottom', 'none'], mode=mode)
        self._label_rotation_mode = mode

    def _get_label_rotation(self):
        """Determine the axis-label rotation and alignment.

        Returns
        -------
        label_rotation : float
            Rotation of the axis label in degree.

        ha : str
            Horizontal alignment of the axis label as a parameter of `Text`.

        va : str
            Vertical alignment of the axis label as a parameter of `Text`.
        """
        # Corners in the pixel coordinates
        corners = self.axes.transAxes.transform(self.axes.corners)

        mode = self._label_rotation_mode
        if mode == 'axis':
            label_rotation, ha, va = _get_label_rotation_along_axis(
                corners, self.axis_name, self.label_position)
        elif mode == 'bottom':
            label_rotation, ha, va = _get_label_rotation_along_bottom(
                corners, self.axis_name, self.label_position)
        else:
            label_rotation = self.label.get_rotation()
            ha = self.label.get_ha()
            va = self.label.get_va()
        return label_rotation, ha, va


class TAxis(TernaryAxis):
    axis_name = 't'


class LAxis(TernaryAxis):
    axis_name = 'l'


class RAxis(TernaryAxis):
    axis_name = 'r'


def _get_label_rotation_along_axis(corners, axis_name, label_position):
    # Index of the corner
    index = {'t': 0, 'l': 1, 'r': 2}[axis_name]
    if label_position == 'tick1':
        c0, c1, c2 = np.roll(corners,  1 - index, axis=0)
    elif label_position == 'tick2':
        c0, c1, c2 = np.roll(corners,  0 - index, axis=0)
    else:  # self.label_position == 'corner':
        c0, c1, c2 = np.roll(corners, -1 - index, axis=0)

    d01 = c1 - c0
    d12 = c2 - c1
    axis_angle = np.rad2deg(np.arctan2(d01[1], d01[0]))  # [-180, +180]
    clockwise = ((d01[0] * d12[1] - d01[1] * d12[0]) < 0.0)
    is_corner = (label_position not in ['tick1', 'tick2'])

    tol = 1e-6
    if abs(abs(axis_angle) - 90.0) < tol:  # axis_angle is -90 or 90.
        # `label_rotation` is determined by comparing the coordinates of
        # the midpoint of the axis with those of the other corner point.
        midpoint = (c0 + c1) * 0.5
        # (the other corner is on the right side) xor
        # (the label is at the other corner)
        if (c2[0] > midpoint[0]) ^ is_corner:
            label_rotation = 90.0
        else:
            label_rotation = -90.0
        va = 'bottom'  # Because the label faces to the axis.
    else:
        # For readability, the angle is adjusted to be in [-90, +90]
        label_rotation = (axis_angle + 90.0) % 180.0 - 90.0
        # (the label rotation is +-180 different from the axis) xor
        # (the triangle is clockwise) xor
        # (the label is at the other corner)
        if (abs(axis_angle) > 90.0) ^ clockwise ^ is_corner:
            va = 'bottom'
        else:
            va = 'top'

    return label_rotation, 'center', va


def _get_label_rotation_along_bottom(corners, axis_name, label_position):
    # Index of the corner
    index = {'t': 0, 'l': 1, 'r': 2}[axis_name]
    if label_position == 'tick1':
        c0, c1, c2 = np.roll(corners,  1 - index, axis=0)
    elif label_position == 'tick2':
        c0, c1, c2 = np.roll(corners,  0 - index, axis=0)
    else:  # elif label_position == 'corner':
        c0, c1, c2 = np.roll(corners, -1 - index, axis=0)

    d01 = c1 - c0
    d12 = c2 - c1
    axis_angle = np.rad2deg(np.arctan2(d01[1], d01[0]))  # [-180, +180]
    clockwise = ((d01[0] * d12[1] - d01[1] * d12[0]) < 0.0)
    is_corner = (label_position not in ['tick1', 'tick2'])

    tol = 1e-6
    b = clockwise ^ is_corner

    if abs(axis_angle) < 75.0 + tol:
        va = 'bottom' if b else 'top'
    elif abs(axis_angle) < 105.0 - tol:
        va = 'center'
    else:
        va = 'top' if b else 'bottom'

    if abs(axis_angle) < 15.0 - tol:
        ha = 'center'
    elif abs(axis_angle) < 165.0 + tol:
        ha = 'right' if (axis_angle < 0.0) ^ b else 'left'
    else:
        ha = 'center'

    return 0.0, ha, va
