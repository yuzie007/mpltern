import numpy as np

from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
from taxes.datasets import get_scatter_points


class TestScatter:
    @image_comparison(baseline_images=['scatter'], style='mpl20')
    def test_scatter(self):
        b, r, l = get_scatter_points()
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.scatter(b, r, l)

    @image_comparison(baseline_images=['scatter_color'], style='mpl20')
    def test_scatter_color(self):
        b, r, l = get_scatter_points()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='ternary')
        sc = ax.scatter(b, r, l, c=range(len(b)))
        colorbar = fig.colorbar(sc, ax=ax, pad=0.15)
        colorbar.set_label('Count', rotation=270, va='baseline')
