import numpy as np

import matplotlib as mpl
from matplotlib import _api
import matplotlib.cbook as cbook
import matplotlib.transforms as mtransforms
from matplotlib.axis import XTick


class TernaryTick(XTick):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tick1line.set_transform(self._get_axis_transform(which='tick1'))
        self.tick2line.set_transform(self._get_axis_transform(which='tick2'))
        self.gridline.set_transform(self._get_axis_transform(which='grid'))

    def _set_labelrotation(self, labelrotation):
        # Overridden to accept `tick` and `axis` as *mode*
        # for the tick-label rotation behavior
        if isinstance(labelrotation, str):
            mode = labelrotation
            angle = 0
        elif isinstance(labelrotation, (tuple, list)):
            mode, angle = labelrotation
        else:
            mode = 'tick'
            angle = labelrotation
        _api.check_in_list(['tick', 'axis', 'horizontal', 'manual'],
                             labelrotation=mode)
        self._labelrotation = (mode, angle)

    def _get_text1_transform(self):
        return {
            'ttick': self.axes.get_taxis_text1_transform,
            'ltick': self.axes.get_laxis_text1_transform,
            'rtick': self.axes.get_raxis_text1_transform,
        }[self.tick_name](self._pad)

    def _get_text2_transform(self):
        return {
            'ttick': self.axes.get_taxis_text2_transform,
            'ltick': self.axes.get_laxis_text2_transform,
            'rtick': self.axes.get_raxis_text2_transform,
        }[self.tick_name](self._pad)

    def _get_axis_transform(self, which):
        """Helper method in `mpltern` to select an appropriate transform."""
        return {
            'ttick': self.axes.get_taxis_transform,
            'ltick': self.axes.get_laxis_transform,
            'rtick': self.axes.get_raxis_transform,
        }[self.tick_name](which=which)

    def _determine_anchor(self, mode, axis_angle, tick_angle):
        """Determine tick-label alignments.

        from the spine and the tick angles.

        Parameters
        ----------
        mode : {'tick', 'axis', 'horizontal'}
        axis_angle : float
            Spine angle in degree.
        tick_angle : float
            Tick angle for `direction="in"` in degree.

        Returns
        -------
        ha : str
            Horizontal alignment.
        va : str
            Vertical alignment.
        rotation : float
        """
        tick_angle = (tick_angle + 180.0) % 360.0 - 180.0  # [-180, 180]
        axis_angle = (axis_angle + 180.0) % 360.0 - 180.0  # [-180, 180]
        tol = 1e-6
        if mode == 'axis':
            is_tick1 = (tick_angle - axis_angle) % 360.0 - 180.0 < 0.0
            if abs(abs(axis_angle) - 90.0) < tol:
                va = 'baseline'
                rotation = 90.0 if is_tick1 ^ (axis_angle > 0.0) else 270.0
            elif abs(axis_angle) < 90.0:
                va = 'top' if is_tick1 else 'baseline'
                rotation = axis_angle
            else:
                va = 'baseline' if is_tick1 else 'top'
                rotation = axis_angle + 180.0
            ha = 'center'
            return ha, va, rotation

        elif mode == 'horizontal':
            # Correct when the triangle is counterclockwise
            is_tick1 = (tick_angle - axis_angle) % 360.0 - 180.0 < 0.0
            is_baseline = (-150.0 + tol < tick_angle < -30.0 - tol)

            # The following part is tuned for regular triangles.
            if is_tick1:
                if axis_angle < -135.0 + tol:
                    ha = 'center'
                    va = 'bottom'
                elif axis_angle < -15.0 - tol:
                    ha = 'right'
                    va = 'baseline' if is_baseline else 'center_baseline'
                elif axis_angle < 45.0 + tol:
                    ha = 'center'
                    va = 'top'
                elif axis_angle < 165.0 - tol:
                    ha = 'left'
                    va = 'baseline' if is_baseline else 'center_baseline'
                else:
                    ha = 'center'
                    va = 'bottom'
            else:
                if axis_angle < -165.0 + tol:
                    ha = 'center'
                    va = 'top'
                elif axis_angle < -45.0 - tol:
                    ha = 'left'
                    va = 'baseline' if is_baseline else 'center_baseline'
                elif axis_angle < 15.0 + tol:
                    ha = 'center'
                    va = 'bottom'
                elif axis_angle < 135.0 - tol:
                    ha = 'right'
                    va = 'baseline' if is_baseline else 'center_baseline'
                else:
                    ha = 'center'
                    va = 'top'
            return ha, va, 0.0

        else:  # mode == 'tick'
            va = 'center_baseline'
            if abs(abs(tick_angle) - 90.0) < tol:
                ha = 'right' if abs(axis_angle) < 0.0 else 'left'
            elif abs(tick_angle) < 90.0:
                ha = 'right'
            else:
                ha = 'left'
            rotation = tick_angle if ha == 'right' else tick_angle + 180.0
            return ha, va, rotation

    def update_position(self, loc):
        # Implementation in `ThetaTick` and `RadialTick` in Matplotlib may be
        # helpful to understand what is done here.
        super().update_position(loc)
        tick1_angle = self.get_tick_angle()  # in degree
        tick2_angle = tick1_angle + 180.0
        axis1_angle = self.get_axis1_angle()  # in degree
        axis2_angle = self.get_axis2_angle()  # in degree
        self._tilt_marker(self.tick1line, np.deg2rad(tick1_angle) - np.pi / 2)
        self._tilt_marker(self.tick2line, np.deg2rad(tick1_angle) + np.pi / 2)

        # Tick labels
        mode, user_angle = self._labelrotation

        if mode == 'manual':
            self.label1.set_rotation(user_angle)
            self.label2.set_rotation(user_angle)
            return

        ha1, va1, rotation1 = self._determine_anchor(
            mode, axis1_angle, tick1_angle)
        self.label1.set_ha(ha1)
        self.label1.set_va(va1)
        self.label1.set_rotation(rotation1 + user_angle)
        self.label1.set_rotation_mode('anchor')

        ha2, va2, rotation2 = self._determine_anchor(
            mode, axis2_angle, tick2_angle)
        self.label2.set_ha(ha2)
        self.label2.set_va(va2)
        self.label2.set_rotation(rotation2 + user_angle)
        self.label2.set_rotation_mode('anchor')

    # Helper methods for `mpltern`

    def get_tick_angle(self):
        # The angle here is for `direction='in'`
        name = self.tick_name
        indices = {'ttick': [2, 1], 'ltick': [0, 2], 'rtick': [1, 0]}[name]
        corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
        points = self.axes.transTernaryAxes.transform(corners)[indices]
        d = points[1] - points[0]
        return np.rad2deg(np.arctan2(d[1], d[0]))

    def get_axis1_angle(self):
        name = self.tick_name
        indices = {'ttick': [2, 0], 'ltick': [0, 1], 'rtick': [1, 2]}[name]
        corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
        points = self.axes.transTernaryAxes.transform(corners)[indices]
        d = points[1] - points[0]
        return np.rad2deg(np.arctan2(d[1], d[0]))

    def get_axis2_angle(self):
        name = self.tick_name
        indices = {'ttick': [1, 0], 'ltick': [2, 1], 'rtick': [0, 2]}[name]
        corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
        points = self.axes.transTernaryAxes.transform(corners)[indices]
        d = points[1] - points[0]
        return np.rad2deg(np.arctan2(d[1], d[0]))

    def _tilt_marker(self, line, angle):
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


class TTick(TernaryTick):
    tick_name = 'ttick'


class LTick(TernaryTick):
    tick_name = 'ltick'


class RTick(TernaryTick):
    tick_name = 'rtick'


