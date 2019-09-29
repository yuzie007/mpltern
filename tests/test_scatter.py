import numpy as np

from matplotlib.testing.decorators import image_comparison
import matplotlib.pyplot as plt
import taxes
import pytest


def get_scatter_points():
    np.random.seed(19680801)
    n = 51
    b = np.random.rand(n)
    r = np.random.rand(n)
    l = np.random.rand(n)
    s = (b + r + l)
    b /= s
    r /= s
    l /= s
    return b, r, l


class TestScatter:
    @image_comparison(baseline_images=['scatter'], style='mpl20')
    def test_scatter(self):
        b, r, l = get_scatter_points()
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.scatter(b, r, l, clip_on=False)

    @image_comparison(baseline_images=['scatter_color'], style='mpl20')
    def test_scatter_color(self):
        b, r, l = get_scatter_points()
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='ternary')
        sc = ax.scatter(b, r, l, c=range(len(b)))
        colorbar = fig.colorbar(sc, ax=ax, pad=0.15)
        colorbar.set_label('Count', rotation=270, va='baseline')
