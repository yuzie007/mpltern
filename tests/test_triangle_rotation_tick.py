import numpy as np

import pytest
from itertools import product
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import mpltern  # noqa: F401


xmin = 0.5 - 1.0 / np.sqrt(3.0)
xmax = 0.5 + 1.0 / np.sqrt(3.0)

corners_dict = dict()
corners_dict['CCW'] = ((0.5, 1.0), (xmin, 0.0), (xmax, 0.0))
corners_dict['CW' ] = ((0.5, 1.0), (xmax, 0.0), (xmin, 0.0))

bs = [False, True]
rotations = range(0, 361, 15)
expected = [(c, b, r, ['{}_{}_{}'.format(c, b, r)])
            for c, b, r in product(['CCW', 'CW'], bs, rotations)]


@pytest.mark.parametrize('corner_label, b, rotation, baseline_images',
                         expected)
@image_comparison(baseline_images=None, extensions=['pdf'], style='mpl20')
def test_triangle_rotation(corner_label, b, rotation, baseline_images):
    corners = corners_dict[corner_label]
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.15, top=0.8)
    ax = fig.add_subplot(
        projection='ternary', corners=corners, rotation=rotation)

    ax.set_tlabel('T')
    ax.set_llabel('L')
    ax.set_rlabel('R')

    ax.tick_params(labelrotation='tick')

    if b:
        ax.taxis.set_ticks_position('tick2')
        ax.laxis.set_ticks_position('tick2')
        ax.raxis.set_ticks_position('tick2')
