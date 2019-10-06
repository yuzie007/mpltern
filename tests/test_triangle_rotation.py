import pytest
from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import taxes

rotations = range(0, 361, 5)
baseline_images_list = [['triangle_rotation_{}'.format(r)] for r in rotations]

# Only pdf is checked because this is the lightest among ['png', 'pdf', 'svg'].
@pytest.mark.parametrize('rotation, baseline_images', zip(rotations, baseline_images_list))
@image_comparison(baseline_images=None, extensions=['pdf'], style='mpl20')
def test_triangle_rotation(rotation, baseline_images):
    fig = plt.figure()
    fig.subplots_adjust(bottom=0.15, top=0.8)
    ax = fig.add_subplot(projection='ternary', rotation=rotation)
    ax.set_tlabel('T')
    ax.set_llabel('L')
    ax.set_rlabel('R')
