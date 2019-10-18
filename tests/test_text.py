import numpy as np

import string
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from mpltern.ternary.axis import _get_points_surrounding_text


def test_text_random():
    np.random.seed(19680801)
    a = list(string.digits + string.ascii_letters
             + string.punctuation.replace('$', '')  # To avoid the math mode
             + ' \n')  # Other whitespaces are unprintable in DejaVu
    has = ['center', 'right', 'left']
    mas = ['center', 'right', 'left']
    rotation_modes = ['default', 'anchor']
    vas = ['top', 'bottom', 'center', 'baseline', 'center_baseline']
    fig = Figure()
    renderer = FigureCanvasAgg(fig).get_renderer()
    for i in range(100):
        x = np.random.rand()
        y = np.random.rand()
        n = np.random.randint(20)
        s = ''.join(np.random.choice(a, n))
        ha = np.random.choice(has)
        ma = np.random.choice(mas)
        va = np.random.choice(vas)
        r = np.random.rand() * 360.0
        rotation_mode = np.random.choice(rotation_modes)
        t = fig.text(x, y, s, ha=ha, ma=ma, va=va, rotation=r,
                     rotation_mode=rotation_mode)
        points = _get_points_surrounding_text(t, renderer)
        bbox = t.get_window_extent(renderer)
        np.testing.assert_almost_equal(np.min(points[:, 0]), bbox.x0)
        np.testing.assert_almost_equal(np.max(points[:, 0]), bbox.x1)
        np.testing.assert_almost_equal(np.min(points[:, 1]), bbox.y0)
        np.testing.assert_almost_equal(np.max(points[:, 1]), bbox.y1)


def test_text_specific():
    """This text is for considering some specific special strings."""
    np.random.seed(19680801)
    # TODO
    ss = ['', ' ', '\n']  # Other whitespaces are unprintable in DejaVu.
    has = ['center', 'right', 'left']
    mas = ['center', 'right', 'left']
    rotation_modes = ['default', 'anchor']
    vas = ['top', 'bottom', 'center', 'baseline', 'center_baseline']
    fig = Figure()
    renderer = FigureCanvasAgg(fig).get_renderer()
    for s in ss:
        for i in range(100):
            x = np.random.rand()
            y = np.random.rand()
            ha = np.random.choice(has)
            ma = np.random.choice(mas)
            va = np.random.choice(vas)
            r = np.random.rand() * 360.0
            rotation_mode = np.random.choice(rotation_modes)
            t = fig.text(x, y, s, ha=ha, ma=ma, va=va, rotation=r,
                         rotation_mode=rotation_mode)
            points = _get_points_surrounding_text(t, renderer)
            bbox = t.get_window_extent(renderer)
            np.testing.assert_almost_equal(np.min(points[:, 0]), bbox.x0)
            np.testing.assert_almost_equal(np.max(points[:, 0]), bbox.x1)
            np.testing.assert_almost_equal(np.min(points[:, 1]), bbox.y0)
            np.testing.assert_almost_equal(np.max(points[:, 1]), bbox.y1)
