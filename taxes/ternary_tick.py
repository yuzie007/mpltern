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
        """Helper method in `taxes` to select an appropriate transform."""
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

    def _determine_anchor(self, mode, axis_angle, tick_angle):
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
        tol = 1e-6
        if mode == 'tick':
            if abs(tick_angle) < 90.0 + tol:
                return 'right', 'center_baseline'
            else:
                return 'left', 'center_baseline'
        elif mode == 'axis':
            if abs(axis_angle) < 90.0:
                return 'center', 'top'
            else:
                return 'center', 'bottom'

        a0 = axis_angle % 180.0  # a0 is within [0, 180]
        tick_angle = (tick_angle + 180.0) % 360.0 - 180.0

        if a0 < 30.0 + tol:
            if (tick_angle - a0) % 360.0 - 180.0 < 0.0:
                return 'center', 'top'
            else:
                return 'center', 'bottom'
        elif a0 < 150.0 - tol:
            # Here `tol` is not needed since it is very unlikely that
            # `tick_angle` and `axis_angle` become the same.
            if (tick_angle - a0) % 360.0 - 180.0 < 0.0:
                ha = 'left'
            else:
                ha = 'right'
            if -150.0 - tol < tick_angle < -30.0 + tol:
                va = 'baseline'
            else:
                va = 'center_baseline'
        else:
            if (tick_angle - a0) % 360.0 - 180.0 < 0.0:
                return 'center', 'bottom'
            else:
                return 'center', 'top'
        return ha, va

    def update_position(self, loc):
        # Implementation in `ThetaTick` and `RadialTick` in Matplotlib may be
        # helpful to understand what is done here.
        super().update_position(loc)
        tick_angle = self.get_tick_angle()  # in degree
        axis1_angle = self.get_axis1_angle()  # in degree
        axis2_angle = self.get_axis2_angle()  # in degree
        self.tilt(self.tick1line, np.deg2rad(tick_angle) - np.pi / 2)
        self.tilt(self.tick2line, np.deg2rad(tick_angle) + np.pi / 2)

        # Tick labels
        mode, user_angle = self._labelrotation
        ha, va = self._determine_anchor(mode, axis1_angle, tick_angle)
        self.label1.set_ha(ha)
        self.label1.set_va(va)
        self.label1.set_rotation_mode('anchor')
        ha, va = self._determine_anchor(mode, axis2_angle, tick_angle + 180.0)
        self.label2.set_ha(ha)
        self.label2.set_va(va)
        self.label2.set_rotation_mode('anchor')
        if mode in 'tick':
            # Adjust `text_angle` within [-90, +90] for readability
            text_angle = (tick_angle + 90.) % 180. - 90.
            self.label1.set_rotation(text_angle + user_angle)
            self.label2.set_rotation(text_angle + user_angle)
        elif mode == 'axis':
            # Adjust `text_angle` within [-90, +90] for readability
            text_angle = (axis1_angle + 90.) % 180. - 90.
            self.label1.set_rotation(text_angle + user_angle)
            text_angle = (axis2_angle + 90.) % 180. - 90.
            self.label2.set_rotation(text_angle + user_angle)
        else:  # mode in ['auto', 'default']
            self.label1.set_rotation(user_angle)
            self.label2.set_rotation(user_angle)

    # Helper methods for `taxes`

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


