"""Spine"""
import matplotlib as mpl
import matplotlib.path as mpath
import matplotlib.spines as mspines


class Spine(mspines.Spine):
    def __init__(self, axes, spine_type, path, **kwargs):
        super().__init__(axes, spine_type, path, **kwargs)
        if spine_type == "tside":
            self.set_transform(self.axes.get_taxis_transform())
        elif spine_type == "lside":
            self.set_transform(self.axes.get_laxis_transform())
        elif spine_type == "rside":
            self.set_transform(self.axes.get_raxis_transform())
        else:
            raise ValueError(f'unknown spine_type: {spine_type}')

    def _adjust_location(self):
        """Automatically set spine bounds to the view interval."""
        if self.spine_type == "tside":
            low = self.axes.get_tlim()[0]
        elif self.spine_type == "lside":
            low = self.axes.get_llim()[0]
        elif self.spine_type == "rside":
            low = self.axes.get_rlim()[0]
        else:
            raise ValueError
        self._path.vertices = [[low, 0.0], [low, 1.0]]

    def get_spine_transform(self):
        return self.get_transform()

    @classmethod
    def linear_spine(cls, axes, spine_type, **kwargs):
        """Create and return a linear `Spine`."""
        path = mpath.Path([(0.0, 0.0), (0.0, 1.0)])
        result = cls(axes, spine_type, path, **kwargs)
        result.set_visible(mpl.rcParams['axes.spines.bottom'])
        return result
