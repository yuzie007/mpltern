import numpy as np

import pytest
from matplotlib.testing.decorators import (
    image_comparison, check_figures_equal)
import matplotlib.pyplot as plt
from mpltern.datasets import (get_spiral, get_triangular_grid)


@image_comparison(baseline_images=['axis_and_tick'], style='mpl20')
def test_axis_and_tick():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='ternary')

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.taxis.set_label_position('tick1')
    ax.laxis.set_label_position('tick1')
    ax.raxis.set_label_position('tick1')

    # Or, you can do
    # ax.taxis.set_label_text('Top')
    # ax.laxis.set_label_text('Left')
    # ax.raxis.set_label_text('Right')


@image_comparison(baseline_images=['plot'], style='mpl20')
def test_plot():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='ternary')
    t, l, r = get_spiral()
    ax.plot(t, l, r)


# In Matplotlib, it is NOT allowed to exchange `x` and `y` in `ax.plot` even
# when specifying them as keyward arguments. Following this behavior, in
# `mpltern`, the order of `t`, `l`, `r` must not be able to exchange.
# The following tests must, therefore, return errors.

# class TestArgumentOrder:
#     # Confirm that the argument order does not affect the plots.
#     @check_figures_equal(extensions=['pdf'])
#     def test_argument_order_1(self, fig_test, fig_ref):
#         t, l, r = get_spiral()
#         fig_test = plt.figure()
#         ax = fig_test.add_subplot(111, projection='ternary')
#         ax.plot(r=r, l=l, t=t)
#         fig_ref = plt.figure()
#         ax = fig_ref.add_subplot(111, projection='ternary')
#         ax.plot(t, l, r)
#
#     # Confirm that the plot is the same even if we have kwargs first.
#     @check_figures_equal(extensions=['pdf'])
#     def test_argument_order_2(self, fig_test, fig_ref):
#         t, l, r = get_spiral()
#         fig_test = plt.figure()
#         ax = fig_test.add_subplot(111, projection='ternary')
#         ax.plot(c='C1', r=r, l=l, t=t)
#         fig_ref = plt.figure()
#         ax = fig_ref.add_subplot(111, projection='ternary')
#         ax.plot(t, l, r, c='C1')


def test_data():
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    t, l, r = get_spiral()
    data = {'t': t, 'l': l, 'r': r}
    ax.plot('t', 'l', 'r', data=data)


def test_data_with_five_arguments():
    # When with data, the number of positional arguments must be 3 or 4.
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    t, l, r = get_spiral()
    data = {'t': t, 'l': l, 'r': r}
    with pytest.raises(ValueError):
        ax.plot('t', 'l', 'r', 'foo', 'bar', data=data)


class TestArguments:
    @image_comparison(baseline_images=['arguments_6'], extensions=['pdf'],
                      style='mpl20')
    def test_arguments_6(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        t, l, r = get_spiral()
        lines = ax.plot(t, l, r, l, r, t)

    @image_comparison(baseline_images=['arguments_7'], extensions=['pdf'],
                      style='mpl20')
    def test_arguments_7(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        t, l, r = get_spiral()
        lines = ax.plot(t, l, r, 'C3:', l, r, t)

    def test_no_arguments(self):
        # In Matplotlib, `ax.plot()` without any arguments returns an empty
        # list. This test checks whether `mpltern` mimics this behavior.
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        lines = ax.plot()
        assert lines == []


class TestTransform:
    # Confirm that `plot` can recognize `ax.transAxes` and handle data
    # ax expected.
    @image_comparison(baseline_images=['transAxes'], extensions=['pdf'],
                      style='mpl20')
    def test_tranform_1(self):
        fig_test = plt.figure()
        ax = fig_test.add_subplot(111, projection='ternary')
        ax.plot([0, 1], [0, 1], transform=ax.transAxes)


class TestGivenTriangles:
    rotations = range(0, 360, 90)
    baseline_images_list = [['given_triangles_{}'.format(r)] for r in rotations]

    # Only pdf is checked because this is the lightest among ['png', 'pdf', 'svg'].
    @pytest.mark.parametrize('rotation, baseline_images', zip(rotations, baseline_images_list))
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


@image_comparison(baseline_images=['corner_labels'], style='mpl20')
def test_corner_labels():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='ternary')

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.taxis.set_label_position('corner')
    ax.laxis.set_label_position('corner')
    ax.raxis.set_label_position('corner')


@image_comparison(baseline_images=['opposite_ticks'], style='mpl20')
def test_opposite_ticks():
    # This changes only tick & label positions but does not change data
    # visualizations.
    # Check if the tick-markers, tick-labels, and axis-labels are shown as
    # expected.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='ternary')

    ax.opposite_ticks(True)

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')


@check_figures_equal()
def test_ternary_lim(fig_test, fig_ref):
    """
    Check that the order of `plot` and `set_ternary_lim` does not affect
    the result.
    """
    ax = fig_test.add_subplot(projection='ternary')
    t, l, r = get_spiral()
    ax.set_ternary_lim(
        0.1, 0.5,  # tmin, tmax
        0.2, 0.6,  # lmin, lmax
        0.3, 0.7,  # rmin, rmax
    )
    ax.plot(t, l, r)
    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax = fig_ref.add_subplot(projection='ternary')
    t, l, r = get_spiral()
    ax.plot(t, l, r)
    ax.set_ternary_lim(
        0.1, 0.5,  # tmin, tmax
        0.2, 0.6,  # lmin, lmax
        0.3, 0.7,  # rmin, rmax
    )
    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')


def set_spans(ax):
    # "clip_on=False" is just for testing purpose
    ax.axtline(0.2, c='C0', clip_on=False)  # line for equi-t values
    ax.axlline(0.3, c='C1', clip_on=False)  # line for equi-l values
    ax.axrline(0.4, c='C2', clip_on=False)  # line for equi-r values

    # "clip_on=False" is just for testing purpose
    ax.axtspan(0.3, 0.4, fc='C0', alpha=0.2, clip_on=False)  # region sandwiched by tmin and tmax
    ax.axlspan(0.4, 0.5, fc='C1', alpha=0.2, clip_on=False)  # region sandwiched by lmin and lmax
    ax.axrspan(0.5, 0.6, fc='C2', alpha=0.2, clip_on=False)  # region sandwiched by rmin and rmax


@image_comparison(baseline_images=['tick_direction'], style='mpl20')
def test_tick_direction():
    fig = plt.figure(figsize=(12.8, 4.8))
    fig.subplots_adjust(left=0.075, right=0.925, wspace=0.5)
    ax = fig.add_subplot(131, projection='ternary')
    ax.tick_params(direction='in')
    ax = fig.add_subplot(132, projection='ternary')
    ax.tick_params(direction='out')  # Default of Matplotlib 2.0+
    ax = fig.add_subplot(133, projection='ternary')
    ax.tick_params(direction='inout')


@image_comparison(baseline_images=['text'], extensions=['pdf'], style='mpl20')
def test_text():
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    v = 1.0 / 3.0
    ax.text(v, v, v, 'center', ha='center', va='center')


class TestArrow:
    @image_comparison(baseline_images=['arrow_data'], extensions=['pdf'],
                      style='mpl20')
    def test_arrow_data(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_ternary_min(-0.2, -0.2, -0.2)
        ax.arrow(0.2, 0.2, 0.8, 0.6, 0.0, -0.6)

    @image_comparison(baseline_images=['arrow_axes'], extensions=['pdf'],
                      style='mpl20')
    def test_arrow_axes(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_ternary_min(-0.2, -0.2, -0.2)
        ax.arrow(0.2, 0.2, 0.8, 0.6, 0.0, -0.6, transform=ax.transTernaryAxes)

    @image_comparison(baseline_images=['arrow_xy_data'], extensions=['pdf'],
                      style='mpl20')
    def test_arrow_xy_data(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_ternary_min(-0.2, -0.2, -0.2)
        ax.arrow(0.2, 0.2, 0.6, 0.6, transform=ax.transData)

    @image_comparison(baseline_images=['arrow_xy_axes'], extensions=['pdf'],
                      style='mpl20')
    def test_arrow_xy_axes(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_ternary_min(-0.2, -0.2, -0.2)
        ax.arrow(0.2, 0.2, 0.6, 0.6, transform=ax.transAxes)


class TestQuiver:
    @image_comparison(baseline_images=['quiver'], extensions=['pdf'],
                      style='mpl20')
    def test_quiver(self):
        t, l, r = get_triangular_grid()
        dt = 1.0 / 3.0 - t
        dl = 1.0 / 3.0 - l
        dr = 1.0 / 3.0 - r
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.quiver(t, l, r, dt, dl, dr)

    @image_comparison(baseline_images=['quiver_color'], extensions=['pdf'],
                      style='mpl20')
    def test_quiver_color(self):
        t, l, r = get_triangular_grid()
        dt = 1.0 / 3.0 - t
        dl = 1.0 / 3.0 - l
        dr = 1.0 / 3.0 - r
        length = np.sqrt(dt ** 2 + dl ** 2 + dr ** 2)
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        pc = ax.quiver(t, l, r, dt, dl, dr, length)
        colorbar = fig.colorbar(pc, pad=0.2)
        colorbar.set_label('Length', rotation=270, va='baseline')

    @image_comparison(baseline_images=['quiver_xy_data'], extensions=['pdf'],
                      style='mpl20')
    def test_quiver_xy_data(self):
        x = np.linspace(0, 1, 11)
        y = np.linspace(0, 1, 11)
        x, y = np.meshgrid(x, y)
        dx = 0.5 - x
        dy = 0.5 - y
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_ternary_min(-0.2, -0.2, -0.2)
        ax.quiver(x, y, dx, dy, transform=ax.transData)

    @image_comparison(baseline_images=['quiver_xy_axes'], extensions=['pdf'],
                      style='mpl20')
    def test_quiver_xy_axes(self):
        x = np.linspace(0, 1, 11)
        y = np.linspace(0, 1, 11)
        x, y = np.meshgrid(x, y)
        dx = 0.5 - x
        dy = 0.5 - y
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_ternary_min(-0.2, -0.2, -0.2)
        ax.quiver(x, y, dx, dy, transform=ax.transAxes)
