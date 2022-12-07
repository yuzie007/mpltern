import numpy as np

import pytest
import matplotlib as mpl
from matplotlib.testing.decorators import (
    image_comparison, check_figures_equal)
import matplotlib.pyplot as plt
from mpltern.ternary.datasets import (
    get_spiral, get_scatter_points, get_triangular_grid)


def fix_text_kerning_factor():
    # `text.kerning_factor` introduced since Matplotlib 3.2.0, changes default
    # text positions. To be compatible with baseline_images, the old behavior
    # is restored.
    if 'text.kerning_factor' in plt.rcParams:
        plt.rcParams['text.kerning_factor'] = 6


@image_comparison(baseline_images=['plot'], extensions=['pdf'], style='mpl20')
def test_plot():
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    t, l, r = get_spiral()
    ax.plot(t, l, r)


# In Matplotlib, it is NOT allowed to exchange `x` and `y` in `ax.plot` even
# when specifying them as keyword arguments. Following this behavior, in
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
        ax.plot(t, l, r, l, r, t)

    @image_comparison(baseline_images=['arguments_7'], extensions=['pdf'],
                      style='mpl20')
    def test_arguments_7(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        t, l, r = get_spiral()
        ax.plot(t, l, r, 'C3:', l, r, t)

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


class TestAxisLabelPosition:
    positions = ['corner', 'tick1', 'tick2']
    baseline_images_list = [
        ['axis_label_position_{}'.format(p)] for p in positions]

    @pytest.mark.parametrize('position, baseline_images',
                             zip(positions, baseline_images_list))
    @image_comparison(baseline_images=None, extensions=['pdf'], style='mpl20')
    def test_axis_label_position(self, position, baseline_images):
        fix_text_kerning_factor()

        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')

        ax.set_tlabel('Top')
        ax.set_llabel('Left')
        ax.set_rlabel('Right')

        ax.taxis.set_label_position(position)
        ax.laxis.set_label_position(position)
        ax.raxis.set_label_position(position)


class TestTitle:
    locs = ['center', 'left', 'right']
    baseline_images_list = [[f'titie_{loc}'] for loc in locs]

    @pytest.mark.parametrize('loc, baseline_images',
                             zip(locs, baseline_images_list),)
    @image_comparison(baseline_images=None, extensions=['pdf'], style='mpl20')
    def test_tick_direction(self, loc, baseline_images):
        fix_text_kerning_factor()

        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_title("Title", loc=loc)


@image_comparison(baseline_images=['aspect'], extensions=['pdf'],
                  style='mpl20')
def test_aspect():
    fix_text_kerning_factor()

    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    ax.plot(*get_spiral())

    ax.set_aspect(1.5)

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')


@image_comparison(baseline_images=['tick_labels_inside_triangle'],
                  extensions=['pdf'], style='mpl20')
def test_tick_labels_inside_triangle():
    fix_text_kerning_factor()

    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.grid()

    ax.tick_params(tick1On=False, tick2On=False)

    # By setting ``labelrotation='manual'``, automatic rotation and alignment
    # for tick labels are prohibited.
    ax.taxis.set_tick_params(labelrotation=('manual',   0.0))
    ax.laxis.set_tick_params(labelrotation=('manual', -60.0))
    ax.raxis.set_tick_params(labelrotation=('manual',  60.0))

    # Then, ``Text`` properties you like can be passed directly by ``update``.
    kwargs = {
        'y': 0.5, 'ha': 'center', 'va': 'center', 'rotation_mode': 'anchor'}
    tkwargs = {'transform': ax.get_taxis_transform()}
    lkwargs = {'transform': ax.get_laxis_transform()}
    rkwargs = {'transform': ax.get_raxis_transform()}
    tkwargs.update(kwargs)
    lkwargs.update(kwargs)
    rkwargs.update(kwargs)
    [text.update(tkwargs) for text in ax.taxis.get_ticklabels()]
    [text.update(lkwargs) for text in ax.laxis.get_ticklabels()]
    [text.update(rkwargs) for text in ax.raxis.get_ticklabels()]


class TestTicks:
    @image_comparison(baseline_images=['opposite_ticks'], extensions=['pdf'],
                      style='mpl20')
    def test_opposite_ticks(self):
        # This changes only tick & label positions but does not change data
        # visualizations.
        # Check if the tick-markers, tick-labels, and axis-labels are shown as
        # expected.
        fix_text_kerning_factor()

        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')

        ax.taxis.set_ticks_position('tick2')
        ax.laxis.set_ticks_position('tick2')
        ax.raxis.set_ticks_position('tick2')

        ax.set_tlabel('Top')
        ax.set_llabel('Left')
        ax.set_rlabel('Right')

    @image_comparison(baseline_images=['negative_ticks'],
                      extensions=['pdf'], style='mpl20')
    def test_negative_ticks(self):
        """
        The previous algorithm for tick-marker rotations did not work as
        expected because it relied on the data coordinates while the sign
        change of x- and/or y-coordinates happened when changing the view
        limits. This should be now fixed by relying not on the data coordiantes
        but on the axes coordinates, and hence it should pass this test.
        """
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_ternary_min(0, 3, -3)

    @image_comparison(baseline_images=['manual_ticks'],
                      extensions=['pdf'], style='mpl20')
    def test_manual_ticks(self):
        fix_text_kerning_factor()

        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')

        ax.plot(*get_spiral())

        ax.grid()

        ax.set_tlabel('Top')
        ax.set_llabel('Left')
        ax.set_rlabel('Right')

        # Specify tick positions manually.
        ax.taxis.set_ticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.laxis.set_ticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.raxis.set_ticks([0.2, 0.4, 0.6, 0.8, 1.0])


@check_figures_equal(extensions=('pdf',))
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
    kwargs = dict(alpha=0.2, clip_on=False)
    ax.axtspan(0.3, 0.4, fc='C0', **kwargs)  # region between tmin and tmax
    ax.axlspan(0.4, 0.5, fc='C1', **kwargs)  # region between lmin and lmax
    ax.axrspan(0.5, 0.6, fc='C2', **kwargs)  # region between rmin and rmax


class TestTickDirection:
    directions = ['in', 'out', 'inout']
    baseline_images_list = [
        ['tick_direction_{}'.format(d)] for d in directions]

    @pytest.mark.parametrize('direction, baseline_images',
                             zip(directions, baseline_images_list))
    @image_comparison(baseline_images=None, extensions=['pdf'], style='mpl20')
    def test_tick_direction(self, direction, baseline_images):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.tick_params(direction=direction)


class TestAxLine:
    @check_figures_equal(extensions=('pdf',))
    def test_axline(self, fig_test, fig_ref):
        ax = fig_test.add_subplot(projection='ternary')
        ax.axline((1.0, 0.0, 0.0), (0.0, 0.5, 0.5))

        ax = fig_ref.add_subplot(projection='ternary')
        ax.plot([1.0, 0.0], [0.0, 0.5], [0.0, 0.5])

    @check_figures_equal(extensions=('pdf',))
    def test_axline_slope(self, fig_test, fig_ref):
        ax = fig_test.add_subplot(projection='ternary')
        ax.axline((1.0, 0.0, 0.0), slope=(-1.0, 0.5, 0.5))

        ax = fig_ref.add_subplot(projection='ternary')
        ax.plot([1.0, 0.0], [0.0, 0.5], [0.0, 0.5])

    @check_figures_equal(extensions=('pdf',))
    def test_axline_axes(self, fig_test, fig_ref):
        ax = fig_test.add_subplot(projection='ternary')
        ax.set_ternary_min(0.1, 0.2, 0.3)
        ax.axline(
            (1.0, 0.0, 0.0),
            (0.0, 0.5, 0.5),
            transform=ax.transTernaryAxes,
        )

        ax = fig_ref.add_subplot(projection='ternary')
        ax.set_ternary_min(0.1, 0.2, 0.3)
        ax.plot([0.5, 0.1], [0.2, 0.4], [0.3, 0.5])

    @check_figures_equal(extensions=('pdf',))
    def test_axline_axes_slope(self, fig_test, fig_ref):
        ax = fig_test.add_subplot(projection='ternary')
        ax.set_ternary_min(0.1, 0.2, 0.3)
        ax.axline(
            (1.0, 0.0, 0.0),
            slope=(-1.0, 0.5, 0.5),
            transform=ax.transTernaryAxes,
        )

        ax = fig_ref.add_subplot(projection='ternary')
        ax.set_ternary_min(0.1, 0.2, 0.3)
        ax.plot([0.5, 0.1], [0.2, 0.4], [0.3, 0.5])

    def test_axline_args(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        with pytest.raises(TypeError):
            ax.axline((1, 0, 0))  # missing second parameter
        with pytest.raises(TypeError):
            # redundant parameters
            ax.axline((1.0, 0.0, 0.0), (0.0, 0.5, 0.5), slope=(-1.0, 0.5, 0.5))
        with pytest.raises(ValueError):
            ax.axline((1, 0, 0), slope=1)
        with pytest.raises(ValueError):
            # two identical points are not allowed
            ax.axline((1, 0, 0), (1, 0, 0))
            plt.draw()


@image_comparison(baseline_images=['text'], extensions=['pdf'], style='mpl20')
def test_text():
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    v = 1.0 / 3.0
    ax.text(v, v, v, 'center', ha='center', va='center')


class TestScatter:
    @image_comparison(baseline_images=['scatter'], extensions=['pdf'],
                      tol=1.0, style='mpl20')
    def test_scatter(self):
        t, l, r = get_scatter_points()
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.scatter(t, l, r)

    @image_comparison(baseline_images=['scatter_color'], extensions=['pdf'],
                      tol=1.0, style='mpl20')
    def test_scatter_color(self):
        fix_text_kerning_factor()

        t, l, r = get_scatter_points()
        fig = plt.figure()
        fig.subplots_adjust(left=0.075, right=0.85)
        ax = fig.add_subplot(111, projection='ternary')
        sc = ax.scatter(t, l, r, c=range(len(t)))
        cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
        colorbar = fig.colorbar(sc, cax=cax)
        colorbar.set_label('Count', rotation=270, va='baseline')

        ax.set_tlabel('Top')
        ax.set_llabel('Left')
        ax.set_rlabel('Right')


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
        ax.arrow(-0.3, 0.2, 0.6, 0.6, transform=ax.transData)

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
                      tol=0.3, style='mpl20')
    def test_quiver_color(self):
        fix_text_kerning_factor()

        t, l, r = get_triangular_grid()
        dt = 1.0 / 3.0 - t
        dl = 1.0 / 3.0 - l
        dr = 1.0 / 3.0 - r
        length = np.sqrt(dt ** 2 + dl ** 2 + dr ** 2)
        fig = plt.figure()
        fig.subplots_adjust(left=0.075, right=0.85)
        ax = fig.add_subplot(projection='ternary')
        pc = ax.quiver(t, l, r, dt, dl, dr, length)
        cax = ax.inset_axes([1.05, 0.1, 0.05, 0.9], transform=ax.transAxes)
        colorbar = fig.colorbar(pc, cax=cax)
        colorbar.set_label('Length', rotation=270, va='baseline')

        ax.set_tlabel('Top')
        ax.set_llabel('Left')
        ax.set_rlabel('Right')

    @image_comparison(baseline_images=['quiver_xy_data'], extensions=['pdf'],
                      style='mpl20')
    def test_quiver_xy_data(self):
        x = np.linspace(-0.5, 0.5, 11)
        y = np.linspace(+0.0, 1.0, 11)
        x, y = np.meshgrid(x, y)
        dx = -x
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


@image_comparison(baseline_images=['legend'], extensions=['pdf'],
                  tol=0.3, style='mpl20')
def test_legend():
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')

    for seed in [1, 9, 6, 8]:
        ax.scatter(*get_scatter_points(11, seed=seed), alpha=0.5, label=seed)

    ax.legend()
