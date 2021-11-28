import pytest
from itertools import product
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


class TestGivenTriangles:
    labelrotations = ['tick', 'axis', 'horizontal']
    rotations = range(0, 360, 90)
    expected = [(lr, r, ['given_triangles_{}_{}'.format(lr, r)])
                for lr, r in product(labelrotations, rotations)]

    @pytest.mark.parametrize('labelrotation, rotation, baseline_images',
                             expected)
    @image_comparison(baseline_images=None, extensions=['pdf'], style='mpl20')
    def test_given_triangles(self, labelrotation, rotation, baseline_images):
        # Check if the tick-markers, tick-labels, and axis-labels are shown as
        # expected.
        if 'text.kerning_factor' in plt.rcParams:
            plt.rcParams['text.kerning_factor'] = 6

        fig = plt.figure()
        corners = ((0.5, 0.0), (1.0, 0.5), (0.0, 1.0))
        ax = fig.add_subplot(
            projection='ternary', corners=corners, rotation=rotation)
        t, l, r = get_spiral()
        ax.plot(t, l, r)

        ax.set_tlabel('Top')
        ax.set_llabel('Left')
        ax.set_rlabel('Right')

        ax.tick_params(labelrotation=labelrotation)

        ax.grid()
