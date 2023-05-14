"""Spine"""
import matplotlib as mpl
import matplotlib.path as mpath
import matplotlib.spines as mspines


class Spine(mspines.Spine):
    def __init__(self, axes, spine_type, path, **kwargs):
        super().__init__(axes, spine_type, path, **kwargs)
        if spine_type in ["tside", "t1"]:
            self.set_transform(self.axes.get_taxis_transform())
        elif spine_type in ["lside", "l1"]:
            self.set_transform(self.axes.get_laxis_transform())
        elif spine_type in ["rside", "r1"]:
            self.set_transform(self.axes.get_raxis_transform())
        else:
            raise ValueError(f'unknown spine_type: {spine_type}')

    def _adjust_location(self):
        """Automatically set spine bounds to the view interval."""
        if self.spine_type in ["tside", "t1"]:
            low, high = self.axes.get_tlim()
        elif self.spine_type in ["lside", "l1"]:
            low, high = self.axes.get_llim()
        elif self.spine_type in ["rside", "r1"]:
            low, high = self.axes.get_rlim()
        else:
            raise ValueError

        if self.spine_type in ["tside", "lside", "rside"]:
            self._path.vertices = [[low, 0.0], [low, 1.0]]
        elif self.spine_type in ["t1", "l1", "r1"]:
            self._path.vertices = [[high, 0.0], [high, 1.0]]
        else:
            raise ValueError

    def get_spine_transform(self):
        return self.get_transform()

    @classmethod
    def linear_spine(cls, axes, spine_type, **kwargs):
        """Create and return a linear `Spine`."""
        path = mpath.Path([(0.0, 0.0), (0.0, 1.0)])
        result = cls(axes, spine_type, path, **kwargs)
        result.set_visible(mpl.rcParams['axes.spines.bottom'])
        return result
