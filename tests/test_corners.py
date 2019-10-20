import pytest
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import get_spiral


class TestGivenTriangles:
    rotations = range(0, 360, 90)
    baseline_images_list = [['given_triangles_{}'.format(r)] for r in rotations]

    @pytest.mark.parametrize('rotation, baseline_images',
                             zip(rotations, baseline_images_list))
    @image_comparison(baseline_images=None, extensions=['pdf'], style='mpl20')
    def test_given_triangles(self, rotation, baseline_images):
        # Check if the tick-markers, tick-labels, and axis-labels are shown as
        # expected.
        fig = plt.figure()
        corners = ((0.5, 0.0), (1.0, 0.5), (0.0, 1.0))
        ax = fig.add_subplot(
            projection='ternary', corners=corners, rotation=rotation)
        t, l, r = get_spiral()
        ax.plot(t, l, r)

        ax.set_tlabel('Top')
        ax.set_llabel('Left')
        ax.set_rlabel('Right')

        ax.grid()


