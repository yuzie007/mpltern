import matplotlib.spines as mspines


class Spine(mspines.Spine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_transform(self.axes.transAxes)

    def _adjust_location(self):
        if True:
            v1 = self._path.vertices
            assert v1.shape == (2, 2), 'unexpected vertices shape'
            if self.spine_type in ['right']:
                v1[0, 0] = self.axes.corners[1][0]
                v1[0, 1] = self.axes.corners[1][1]
                v1[1, 0] = self.axes.corners[2][0]
                v1[1, 1] = self.axes.corners[2][1]
            elif self.spine_type in ['left']:
                v1[0, 0] = self.axes.corners[2][0]
                v1[0, 1] = self.axes.corners[2][1]
                v1[1, 0] = self.axes.corners[0][0]
                v1[1, 1] = self.axes.corners[0][1]
            elif self.spine_type in ['top', 'bottom']:  # TODO
                v1[0, 0] = self.axes.corners[0][0]
                v1[0, 1] = self.axes.corners[0][1]
                v1[1, 0] = self.axes.corners[1][0]
                v1[1, 1] = self.axes.corners[1][1]
            else:
                raise ValueError('unable to set bounds for spine "%s"' %
                                 self.spine_type)

    def get_spine_transform(self):
        return self.axes.transAxes
