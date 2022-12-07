import numpy as np

import matplotlib as mpl
from matplotlib import _api
import matplotlib.cbook as cbook
from matplotlib.axis import XAxis
import matplotlib.text as mtext
import matplotlib.ticker as mticker
from matplotlib.transforms import Affine2D
from mpltern.ternary.tick import TTick, LTick, RTick


class TernaryAxis(XAxis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # x : data coordinates in the axis direction
        # y : display (pixel) coordinates in the direction vertical to the
        #     axis direction, updated when drawn in `_update_label_positions`
        trans = {
            't': self.axes.get_taxis_transform(which='label'),
            'l': self.axes.get_laxis_transform(which='label'),
            'r': self.axes.get_raxis_transform(which='label'),
        }[self.axis_name]
        self.label.set_rotation(0)
        self.label.set_rotation_mode('anchor')
        self.label.set_transform(trans)
        self.label_position = 'corner'
        self._label_rotation_mode = 'axis'

    def _copy_tick_props(self, src, dest):
        super()._copy_tick_props(src, dest)
        dest.label1.set_y(src.label1.get_position()[1])
        dest.label2.set_y(src.label2.get_position()[1])

    def set_ticks(self, ticks, minor=False):
        """
        Set the locations of the tick marks from sequence ticks

        Parameters
        ----------
        ticks : sequence of floats
        minor : bool
        """
        if minor:
            self.set_minor_locator(mticker.FixedLocator(ticks))
            return self.get_minor_ticks(len(ticks))
        else:
            self.set_major_locator(mticker.FixedLocator(ticks))
            return self.get_major_ticks(len(ticks))

    def _get_tick(self, major):
        if major:
            tick_kw = self._major_tick_kw
        else:
            tick_kw = self._minor_tick_kw
        tick = {
            't': TTick,
            'l': LTick,
            'r': RTick,
        }[self.axis_name]
        try:
            return tick(self.axes, 0, major=major, **tick_kw)
        except TypeError:  # matplotlib<=3.2.2
            return tick(self.axes, 0, '', major=major, **tick_kw)

    def set_label_position(self, position):
        """
        Set the label position (corner, tick1, or tick2)

        Parameters
        ----------
        position : {'corner', 'tick1', 'tick2'}
        """
        _api.check_in_list(['corner', 'tick1', 'tick2'], position=position)
        self.label_position = position
        self.stale = True

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
            corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
            corners = self.axes.transTernaryAxes.transform(corners)
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
        Set the ticks position.

        Parameters
        ----------
        position : {'tick1', 'tick2', 'both', 'default', 'none'}
            'both' sets the ticks to appear on both positions, but does not
            change the tick labels.  'default' resets the tick positions to
            the default.                                             'none'
            can be used if you don't want any ticks. 'none' and 'both'
            affect only the ticks, not the labels.
        """
        _api.check_in_list(
            ['tick1', 'tick2', 'both', 'default', 'none'],
            position=position,
        )
        if position in ['tick1', 'default']:
            self.set_tick_params(which='both', tick1On=True, label1On=True,
                                 tick2On=False, label2On=False)
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
            assert False, "unhandled parameter not caught by _check_in_list"
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
        ticks = []
        # Only ticks to draw are added.
        for axis in self.axes._get_axis_list():
            if axis in [self.axes.xaxis, self.axes.yaxis]:
                continue
            try:
                ticks.extend(axis._update_ticks())
            except TypeError:  # For Matplotlib 3.0.3
                ticks.extend(axis._update_ticks(renderer))
        points = []
        for tick in ticks:
            for text in [tick.label1, tick.label2]:
                if text.get_visible():
                    points.extend(_get_points_surrounding_text(text, renderer))
        # In case no tick labels exist, points of triangle corners are added.
        corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
        points.extend(self.axes.transTernaryAxes.transform(corners))
        return np.asarray(points)

    def set_label_rotation_mode(self, mode):
        """
        Set the mode how to rotate and align the axis-label.

        Parameters
        ----------
        mode : {'axis', 'horizontal', 'manual'}
        """
        _api.check_in_list(['axis', 'horizontal', 'manual'], mode=mode)
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
        corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
        corners = self.axes.transTernaryAxes.transform(corners)

        mode = self._label_rotation_mode
        if mode == 'axis':
            label_rotation, ha, va = _get_label_rotation_along_axis(
                corners, self.axis_name, self.label_position)
        elif mode == 'horizontal':
            label_rotation, ha, va = _get_label_rotation_horizontal(
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


def _get_label_rotation_horizontal(corners, axis_name, label_position):
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


def _get_points_surrounding_text(text: mtext.Text, renderer):
    """
    Get the points surrounding ``text`` in the display (pixel) coordinates.

    This method is extracted and modified from ``mtext._get_textbox``.

    ``parts`` is the list of:
        - ``t`` : string of each line
        - ``wh`` : width and height of ``text`` without rotation. In the
          height, the descent is not included and therefore have to be
          subtracted to get ``ymin``.
        - ``x`` and ``y`` : ``xmin`` and ``ymax`` relative to ``position``
          after the ``text`` rotation and alignment. (0, 0) is the rotation
          center.

    ``position`` : absolute position of ``text`` in the display coordinates.
        The ``parts`` above are relative coordinates to ``position``.

    1. We must get the four corners surrounding ``text``. For this, we first
      rotate back the ``text`` box and find ``xmin``, ``ymin``, ``xmax``,
      ``ymax``.
    2. Then we rotate again the four points.
    3. Add the absolute position of ``text`` to the rotated four points and
       return them.
    """
    tr = Affine2D().rotate_deg(-text.get_rotation())

    _, parts, d = text._get_layout(renderer)

    # In ``Text.get_window_extent``, if the empty text is given, it just
    # returns ``Bbox`` with no width and no height.
    # To be consistent, here also empty box is given for empty text.
    if text.get_text() == '':
        xmin = ymin = xmax = ymax = 0.0

    else:
        projected_xs = []
        projected_ys = []
        for t, wh, x, y in parts:
            w, h = wh

            xt1, yt1 = tr.transform_point((x, y))
            yt1 -= d
            xt2, yt2 = xt1 + w, yt1 + h

            projected_xs.extend([xt1, xt2])
            projected_ys.extend([yt1, yt2])

        xmin, ymin = min(projected_xs), min(projected_ys)
        xmax, ymax = max(projected_xs), max(projected_ys)

    position = text.get_transform().transform(text.get_position())
    points = np.array([[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]])
    return tr.inverted().transform(points) + position
