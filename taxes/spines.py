import matplotlib.spines as mspines


class Spine(mspines.Spine):
    def _adjust_location(self):
        if True:
            v1 = self._path.vertices
            assert v1.shape == (2, 2), 'unexpected vertices shape'
            if self.spine_type in ['right']:
                v1[0, 0] = self.axes.viewLim.intervalx[1]
                v1[0, 1] = self.axes.viewLim.intervaly[0]
                v1[1, 0] = sum(self.axes.viewLim.intervalx) * 0.5
                v1[1, 1] = self.axes.viewLim.intervaly[1]
            elif self.spine_type in ['left']:
                v1[0, 0] = sum(self.axes.viewLim.intervalx) * 0.5
                v1[0, 1] = self.axes.viewLim.intervaly[1]
                v1[1, 0] = self.axes.viewLim.intervalx[0]
                v1[1, 1] = self.axes.viewLim.intervaly[0]
            elif self.spine_type in ['bottom']:
                v1[0, 0] = self.axes.viewLim.intervalx[0]
                v1[0, 1] = self.axes.viewLim.intervaly[0]
                v1[1, 0] = self.axes.viewLim.intervalx[1]
                v1[1, 1] = self.axes.viewLim.intervaly[0]
            elif self.spine_type in ['top']:
                pass
            else:
                raise ValueError('unable to set bounds for spine "%s"' %
                                 self.spine_type)

    def get_spine_transform(self):
        return self.axes.transData
