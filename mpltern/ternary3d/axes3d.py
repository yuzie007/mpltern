import numpy as np

import matplotlib.transforms as mtransforms
from mpl_toolkits.mplot3d.axes3d import Axes3D
from mpltern.ternary.transforms import BarycentricTransform
from mpltern.ternary._base import _create_corners
from mpltern._ternary_parsers import _get_xy


class TernaryAxes3D(Axes3D):
    name = 'ternary3d'

    def __init__(self, *args, ternary_sum: float = 1.0, corners=None,
                 rotation: float = None, **kwargs):
        """3D ternary axes object.

        Parameters
        ----------
        ternary_sum : float, optional
            Constant to which ``t + l + r`` is normalized, by default 1.0
        corners : Sequence[float] or None, optional
            Corners of the triangle, by default None
        rotation : float or None, optional
            Rotation angle of the triangle, by default None
        """
        # Since Matplotlib 3.5.0, `auto_add_to_figure` is "deprecated" but
        # actually causes an error if it is `True`.
        # To avoid this we set `False` to this argument.
        # Since Matplotlib 3.6.0, `auto_add_to_figure` is not necessary to set.
        kwargs.setdefault('auto_add_to_figure', False)

        # Triangle corners in the original data coordinates
        self.corners_data = _create_corners(corners, rotation)
        sx = np.sqrt(3.0) * 0.5  # Scale for x
        xmin = -1.0 / np.sqrt(3.0)
        v = xmin * sx
        trans = mtransforms.Affine2D().from_values(sx, 0.0, 0.0, 1.0, -v, 0.0)
        # Triangle corners in the original ``Axes`` coordinates
        self.corners_axes = trans.transform(self.corners_data)

        self.ternary_sum = ternary_sum
        super().__init__(*args, **kwargs)

    def _set_lim_and_transforms(self):
        super()._set_lim_and_transforms()

        corners_axes = self.corners_axes

        # From ternary coordinates to the original data coordinates
        self.transProjection = BarycentricTransform(self.corners_data)

        # From barycentric coordinates to the original Axes coordinates
        self.transAxesProjection = BarycentricTransform(corners_axes.copy())

        # From barycentric coordinates to display coordinates
        self.transTernaryAxes = self.transAxesProjection + self.transAxes

    def plot(self, *args, **kwargs):
        trans = kwargs.pop('transform', None)
        this, args = args[:3], args[3:]
        x, y, kwargs['transform'] = _get_xy(self, this, trans)
        args = (x, y, *args)
        return super().plot(*args, **kwargs)
