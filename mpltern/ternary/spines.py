from matplotlib import rcParams
import matplotlib.spines as mspines
import matplotlib.path as mpath


class Spine(mspines.Spine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_transform(self.axes.transAxes)

    def _adjust_location(self):
        corners = [[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]]
        corners_axes = self.axes.transAxesProjection.transform(corners)

        v1 = self._path.vertices
        assert v1.shape == (2, 2), 'unexpected vertices shape'
        if self.spine_type in ['tside']:
            v1[0] = corners_axes[1]
            v1[1] = corners_axes[2]
        elif self.spine_type in ['lside']:
            v1[0] = corners_axes[2]
            v1[1] = corners_axes[0]
        elif self.spine_type in ['rside']:
            v1[0] = corners_axes[0]
            v1[1] = corners_axes[1]
        else:
            raise ValueError('unable to set bounds for spine "%s"' %
                             self.spine_type)

    def get_spine_transform(self):
        return self.axes.transAxes

    @classmethod
    def linear_spine(cls, axes, spine_type, **kwargs):
        """
        (staticmethod) Returns a linear :class:`Spine`.
        """
        # all values of 0.999 get replaced upon call to set_bounds()
        if spine_type == 'tside':
            path = mpath.Path([(0.0, 0.0), (1.0, 0.0)])
        elif spine_type == 'lside':
            path = mpath.Path([(0.5, 1.0), (0.0, 0.0)])
        elif spine_type == 'rside':
            path = mpath.Path([(1.0, 0.0), (0.5, 1.0)])
        else:
            raise ValueError('unable to make path for spine "%s"' % spine_type)
        result = cls(axes, spine_type, path, **kwargs)
        result.set_visible(rcParams['axes.spines.bottom'])

        return result

