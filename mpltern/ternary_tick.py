import numpy as np

import matplotlib.cbook as cbook
import matplotlib.transforms as mtransforms
from matplotlib.axis import XTick


class TernaryTick(XTick):
    def _set_labelrotation(self, labelrotation):
        # Overridden to accept `tick` and `axis` as *mode*
        # for the tick-label rotation behavior
        if isinstance(labelrotation, str):
            mode = labelrotation
            angle = 0
        elif isinstance(labelrotation, (tuple, list)):
            mode, angle = labelrotation
        else:
            mode = 'default'
            angle = labelrotation
        cbook._check_in_list(['auto', 'default', 'tick', 'axis'],
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

    def _get_tick1line(self):
        l = super()._get_tick1line()
        l.set_transform(self._get_axis_transform(which='tick1'))
        return l

    def _get_tick2line(self):
        l = super()._get_tick2line()
        l.set_transform(self._get_axis_transform(which='tick2'))
        return l

    def _get_gridline(self):
        l = super()._get_gridline()
        l.set_transform(self._get_axis_transform(which='grid'))
        return l

    def _determine_anchor(self, mode, axis_angle, tick_angle, tick_index):
        """Determine tick-label alignments.

        from the spine and the tick angles.

        Parameters
        ----------
        mode : {'auto', 'default', 'tick', 'axis'}
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
        """
        tick_angle = (tick_angle + 180.0) % 360.0 - 180.0  # [-180, 180]
        axis_angle = (axis_angle + 180.0) % 360.0 - 180.0  # [-180, 180]
        tol = 1e-6
        if mode == 'tick':
            va = 'center_baseline'
            if abs(tick_angle - 90.0) < tol:
                ha = 'right' if tick_angle < 0.0 else 'left'
            elif abs(tick_angle) < 90.0:
                ha = 'right'
            else:
                ha = 'left'
            return ha, va
        elif mode == 'axis':
            index = {'ttick': 0, 'ltick': 1, 'rtick': 2}[self.tick_name]
            i0 = (index + 0) % 3
            i1 = (index + 1) % 3
            i2 = (index + 2) % 3
            corners = self.axes.corners
            c0 = corners[i0]
            c1 = corners[i1]
            c2 = corners[i2]
            if tick_index == 1:
                midpoint = (c2 + c0) * 0.5
                xy = -(c1 - midpoint) + midpoint
            else:
                midpoint = (c0 + c1) * 0.5
                xy = -(c2 - midpoint) + midpoint
            if abs(xy[1] - midpoint[1]) < tol:  # same *y* coordinate
                label_rotation = 90.0 if xy[0] < midpoint[0] else 270.0
                va = 'baseline'  # As the label may be rotated by 90 deg.
            else:
                # For readability, the angle is adjusted to be in [-90, +90]
                label_rotation = (axis_angle + 90.0) % 180.0 - 90.0
                if xy[1] < midpoint[1]:  # lower of the axis
                    va = 'top'
                else:
                    va = 'baseline'
            ha = 'center'
            return ha, va

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
        return ha, va

    def update_position(self, loc):
        # Implementation in `ThetaTick` and `RadialTick` in Matplotlib may be
        # helpful to understand what is done here.
        super().update_position(loc)
        tick1_angle = self.get_tick_angle()  # in degree
        tick2_angle = tick1_angle + 180.0
        axis1_angle = self.get_axis1_angle()  # in degree
        axis2_angle = self.get_axis2_angle()  # in degree
        self.tilt(self.tick1line, np.deg2rad(tick1_angle) - np.pi / 2)
        self.tilt(self.tick2line, np.deg2rad(tick1_angle) + np.pi / 2)

        # Tick labels
        mode, user_angle = self._labelrotation
        ha1, va1 = self._determine_anchor(mode, axis1_angle, tick1_angle, 1)
        self.label1.set_ha(ha1)
        self.label1.set_va(va1)
        self.label1.set_rotation_mode('anchor')
        ha2, va2 = self._determine_anchor(mode, axis2_angle, tick2_angle, 2)
        self.label2.set_ha(ha2)
        self.label2.set_va(va2)
        self.label2.set_rotation_mode('anchor')
        if mode in 'tick':
            text_angle = tick1_angle if ha1 == 'right' else tick2_angle
            self.label1.set_rotation(text_angle + user_angle)
            text_angle = tick2_angle if ha2 == 'right' else tick1_angle
            self.label2.set_rotation(text_angle + user_angle)
        elif mode == 'axis':
            tol = 1e-6
            text_angle = (axis1_angle + 90.) % 180. - 90.
            if abs(text_angle) > 90.0 - tol:
                text_angle = 90.0 if tick1_angle < 0.0 else 270.0
            self.label1.set_rotation(text_angle + user_angle)
            text_angle = (axis2_angle + 90.) % 180. - 90.
            if abs(text_angle) > 90.0 - tol:
                text_angle = 90.0 if tick2_angle < 0.0 else 270.0
            self.label2.set_rotation(text_angle + user_angle)
        else:  # mode in ['auto', 'default']
            self.label1.set_rotation(user_angle)
            self.label2.set_rotation(user_angle)

    # Helper methods for `mpltern`

    def get_tick_angle(self):
        # The angle here is for `direction='in'`
        trans = self._get_axis_transform(which='grid')
        points = trans.transform([[0., 0.], [0., 1.]])
        d = points[1] - points[0]
        return np.rad2deg(np.arctan2(d[1], d[0]))

    def get_axis1_angle(self):
        trans = self._get_axis_transform(which='grid')
        points = trans.transform([[0., 0.], [1., 0.]])
        d = points[1] - points[0]
        return np.rad2deg(np.arctan2(d[1], d[0]))

    def get_axis2_angle(self):
        trans = self._get_axis_transform(which='grid')
        points = trans.transform([[0., 1.], [1., 1.]])
        d = points[1] - points[0]
        return np.rad2deg(np.arctan2(d[1], d[0]))

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


class TTick(TernaryTick):
    tick_name = 'ttick'


class LTick(TernaryTick):
    tick_name = 'ltick'


class RTick(TernaryTick):
    tick_name = 'rtick'


