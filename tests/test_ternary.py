import numpy as np

import pytest
import matplotlib as mpl
from matplotlib.testing.decorators import (
    image_comparison, check_figures_equal)
import matplotlib.pyplot as plt
from mpltern.datasets import (
    get_spiral, get_scatter_points, get_triangular_grid)


def fix_text_kerning_factor():
    # `text.kerning_factor` introduced since Matplotlib 3.2.0, changes default
    # text positions. To be compatible with baseline_images, the old behavior
    # is restored.
    if 'text.kerning_factor' in plt.rcParams:
        plt.rcParams['text.kerning_factor'] = 6


@image_comparison(baseline_images=['plot'], extensions=['pdf'], style='mpl20')
def test_plot():
    """Test if `plot` works as expected."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    tn0, tn1, tn2 = get_spiral()
    ax.plot(tn0, tn1, tn2)


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


@check_figures_equal(extensions=('pdf',))
def test_data(fig_ref, fig_test):
    """Test if the `data` argument works correctly."""
    tn0, tn1, tn2 = get_spiral()

    ax = fig_test.add_subplot(projection='ternary')
    data = {'tn0': tn0, 'tn1': tn1, 'tn2': tn2}
    ax.plot('tn0', 'tn1', 'tn2', data=data)

    ax = fig_ref.add_subplot(projection='ternary')
    ax.plot(tn0, tn1, tn2)


def test_data_with_five_arguments():
    """Test if data with 5 arguments raise ValueError.

    With data, the number of positional arguments must be 3 or 4.
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    tn0, tn1, tn2 = get_spiral()
    data = {'tn0': tn0, 'tn1': tn1, 'tn2': tn2}
    with pytest.raises(ValueError):
        ax.plot('tn0', 'tn1', 'tn2', 'foo', 'bar', data=data)


class TestArguments:
    @image_comparison(baseline_images=['arguments_6'], extensions=['pdf'],
                      style='mpl20')
    def test_arguments_6(self):
        """Test if 6 arguments are parsed correctly."""
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        tn0, tn1, tn2 = get_spiral()
        ax.plot(tn0, tn1, tn2, tn1, tn2, tn0)

    @image_comparison(baseline_images=['arguments_7'], extensions=['pdf'],
                      style='mpl20')
    def test_arguments_7(self):
        """Test if 7 arguments are parsed correctly."""
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        tn0, tn1, tn2 = get_spiral()
        ax.plot(tn0, tn1, tn2, 'C3:', tn1, tn2, tn0)

    def test_no_arguments(self):
        """Test if `plot` with no arguments returns an empty list."""
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        lines = ax.plot()
        assert lines == []


class TestTransform:
    @image_comparison(baseline_images=['transAxes'], extensions=['pdf'],
                      style='mpl20')
    def test_tranform_1(self):
        """Test if `plot` recognizes and handle `ax.transAxes` as expected."""
        fig_test = plt.figure()
        ax = fig_test.add_subplot(111, projection='ternary')
        ax.plot([0, 1], [0, 1], transform=ax.transAxes)


class TestAxisLabelPosition:
    positions = ['corner', 'tick1', 'tick2']
    baseline_images_list = [[f'axis_label_position_{p}'] for p in positions]

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
    def test_title_loc(self, loc, baseline_images):
        fix_text_kerning_factor()

        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.set_title("Title", loc=loc)


@image_comparison(baseline_images=['aspect'], extensions=['pdf'],
                  style='mpl20')
def test_aspect():
    """Test if `set_aspect` works."""
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
        """Test if "tick2" works.

        "tick2" should change the positions of tick-markers, tick-labels, and
        axis-labels but should not change data points.
        """
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
        """Test if ticks can be manually given."""
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

    @image_comparison(baseline_images=['manual_ticklabels'],
                      extensions=['pdf'], style='mpl20')
    def test_manual_ticklabels(self):
        """Test if tick-labels can be manually given."""
        fix_text_kerning_factor()

        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')

        # Specify tick positions manually.
        ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
        labels = ["0/5", "1/5", "2/5", "3/5", "4/5", "5/5"]
        ax.taxis.set_ticks(ticks, labels=labels)
        ax.laxis.set_ticks(ticks, labels=labels)
        ax.raxis.set_ticks(ticks, labels=labels)

    @mpl.style.context("default")
    @check_figures_equal(extensions=('pdf',))
    def test_number_of_ticks(self, fig_test, fig_ref):
        """
        Test if the number of ticks are automatically properly adjusted.

        It is necessary to switch the style to "default" because the "classic"
        style gives a different result.
        """
        ax = fig_test.add_subplot(projection="ternary")
        ax.set_ternary_lim(0.0, 0.2, 0.0, 1.0, 0.0, 1.0)

        ax = fig_ref.add_subplot(projection="ternary")
        ax.set_ternary_lim(0.0, 0.2, 0.0, 1.0, 0.0, 1.0)
        ax.taxis.set_ticks([0.0, 0.1, 0.2])


@check_figures_equal(extensions=('pdf',))
def test_ternary_sum(fig_test, fig_ref):
    """Test if the `ternary_sum` argument works correctly."""
    ax = fig_test.add_subplot(projection='ternary', ternary_sum=0.5)
    tn0, tn1, tn2 = get_spiral()
    ax.plot(tn0, tn1, tn2)
    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax = fig_ref.add_subplot(projection='ternary')
    tn0, tn1, tn2 = get_spiral()
    ax.plot(tn0, tn1, tn2)
    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')
    ticks = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    ticklabels = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    ax.taxis.set_ticks(ticks, ticklabels)
    ax.laxis.set_ticks(ticks, ticklabels)
    ax.raxis.set_ticks(ticks, ticklabels)


class TestTernaryLim:
    @check_figures_equal(extensions=('pdf',))
    def test_order_data(self, fig_test, fig_ref):
        """
        Check that the order of `plot` and `set_ternary_lim` does not affect
        the result.
        """
        tn0, tn1, tn2 = get_spiral()

        ax = fig_test.add_subplot(projection="ternary")
        ax.set_ternary_lim(
            0.1, 0.5,  # tmin, tmax
            0.2, 0.6,  # lmin, lmax
            0.3, 0.7,  # rmin, rmax
        )
        ax.plot(tn0, tn1, tn2)

        ax = fig_ref.add_subplot(projection="ternary")
        ax.plot(tn0, tn1, tn2)
        ax.set_ternary_lim(
            0.1, 0.5,  # tmin, tmax
            0.2, 0.6,  # lmin, lmax
            0.3, 0.7,  # rmin, rmax
        )

    @check_figures_equal(extensions=('pdf',))
    def test_order_axes(self, fig_test, fig_ref):
        tn0, tn1, tn2 = get_spiral()

        ax = fig_test.add_subplot(projection="ternary")
        ax.set_ternary_lim(0.1, 0.7, 0.1, 0.6, 0.1, 0.5)
        ax.plot(tn0, tn1, tn2)
        ax.plot(tn0, tn1, tn2, "k", transform=ax.transTernaryAxes)

        ax = fig_ref.add_subplot(projection="ternary")
        ax.plot(tn0, tn1, tn2)
        ax.plot(tn0, tn1, tn2, "k", transform=ax.transTernaryAxes)
        ax.set_ternary_lim(0.1, 0.7, 0.1, 0.6, 0.1, 0.5)

    @check_figures_equal(extensions=('pdf',))
    def test_order_limits(self, fig_test, fig_ref):
        """Test if the plot is insensitive to the orders of limits."""
        ax = fig_test.add_subplot(projection="ternary")
        ax.set_ternary_lim(0.1, 0.7, 0.1, 0.6, 0.1, 0.5)

        ax = fig_ref.add_subplot(projection="ternary")
        ax.set_ternary_lim(0.7, 0.1, 0.6, 0.1, 0.5, 0.1)

    @check_figures_equal(extensions=('pdf',))
    def test_min_vs_max(self, fig_test, fig_ref):
        """Test if ternary_min and ternary_max give the same result."""
        ax = fig_test.add_subplot(projection="ternary")
        ax.set_ternary_min(0.1, 0.2, 0.3)

        ax = fig_ref.add_subplot(projection="ternary")
        ax.set_ternary_max(0.5, 0.6, 0.7)

    @pytest.mark.parametrize(
        "fit, baseline_images", [
            ["rectangle", ["fit_rectangle"]],
            ["triangle", ["fit_triangle"]],
            ["none", ["fit_none"]],
        ],
    )
    @image_comparison(
        baseline_images=None,
        extensions=['pdf'],
        remove_text=True,
        style='mpl20',
    )
    def test_fit(self, fit: str, baseline_images):
        """Test if hexagonal limits are properly plotted."""
        fig = plt.figure()
        ax = fig.add_subplot(projection="ternary")
        tn0, tn1, tn2 = get_spiral()
        ax.plot(tn0, tn1, tn2, "C0")
        ax.plot(tn0, tn1, tn2, "k", transform=ax.transTernaryAxes)
        ax.set_facecolor("0.9")
        ax.grid(True)
        ax.set_ternary_lim(0.1, 0.7, 0.1, 0.6, 0.1, 0.5, fit)

    @pytest.mark.parametrize("fit", ["rectangle", "triangle", "none"])
    @check_figures_equal(extensions=('pdf',))
    def test_ternary_lim_vs_tlrlims_0(self, fig_test, fig_ref, fit):
        """Test if the plot is insensitive to the orders of limits."""
        ax = fig_test.add_subplot(projection="ternary")
        ax.set_tlim(0.1, 0.5, fit)
        ax.set_llim(0.2, 0.6, fit)
        ax.set_rlim(0.3, 0.7, fit)

        ax = fig_ref.add_subplot(projection="ternary")
        ax.set_ternary_lim(0.1, 0.5, 0.2, 0.6, 0.3, 0.7, fit)

    @pytest.mark.parametrize("fit", ["rectangle", "triangle", "none"])
    @check_figures_equal(extensions=('pdf',))
    def test_ternary_lim_vs_tlrlims_1(self, fig_test, fig_ref, fit):
        """Test if the plot is insensitive to the orders of limits."""
        ax = fig_test.add_subplot(projection="ternary")
        ax.set_tlim(0.1, 0.7, fit)
        ax.set_llim(0.1, 0.6, fit)
        ax.set_rlim(0.1, 0.5, fit)

        ax = fig_ref.add_subplot(projection="ternary")
        ax.set_ternary_lim(0.1, 0.7, 0.1, 0.6, 0.1, 0.5, fit)


class TestSpans:
    """Tests related to spans."""
    @image_comparison(
        baseline_images=['spans'],
        extensions=['pdf'],
        remove_text=True,
        style='mpl20',
    )
    def test_spans(self):
        """Test if spans are plotted properly."""
        fig = plt.figure()
        ax = fig.add_subplot(projection="ternary")

        ax.axtline(0.2, c='C0')
        ax.axlline(0.3, c='C1')
        ax.axrline(0.4, c='C2')

        ax.axtspan(0.3, 0.5, fc='C0', alpha=0.2)
        ax.axlspan(0.4, 0.6, fc='C1', alpha=0.2)
        ax.axrspan(0.5, 0.7, fc='C2', alpha=0.2)

    def test_axtline_transform(self):
        """Test if `axtline` raises `ValueError` when getting `transform`"""
        fig = plt.figure()
        ax = fig.add_subplot(projection="ternary")
        with pytest.raises(ValueError):
            ax.axtline(0.5, transform=ax.transAxes)

    def test_axlline_transform(self):
        """Test if `axlline` raises `ValueError` when getting `transform`"""
        fig = plt.figure()
        ax = fig.add_subplot(projection="ternary")
        with pytest.raises(ValueError):
            ax.axlline(0.5, transform=ax.transAxes)

    def test_axrline_transform(self):
        """Test if `axrline` raises `ValueError` when getting `transform`"""
        fig = plt.figure()
        ax = fig.add_subplot(projection="ternary")
        with pytest.raises(ValueError):
            ax.axrline(0.5, transform=ax.transAxes)


class TestTickDirection:
    directions = ['in', 'out', 'inout']
    baseline_images_list = [[f'tick_direction_{d}'] for d in directions]

    @pytest.mark.parametrize('direction, baseline_images',
                             zip(directions, baseline_images_list))
    @image_comparison(baseline_images=None, extensions=['pdf'], style='mpl20')
    def test_tick_direction(self, direction, baseline_images):
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.tick_params(direction=direction)


class TestAxisLabels:
    """Test if ternary axis labels are assigned properly."""
    def test_tlabel(self):
        """Test if the t-axis label is assigned properly."""
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        label = "T"
        ax.set_tlabel(label)
        assert ax.get_tlabel() == label

    def test_llabel(self):
        """Test if the l-axis label is assigned properly."""
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        label = "L"
        ax.set_llabel(label)
        assert ax.get_llabel() == label

    def test_rlabel(self):
        """Test if the r-axis label is assigned properly."""
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        label = "R"
        ax.set_rlabel(label)
        assert ax.get_rlabel() == label


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
    """Test if text is plotted correctly."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')
    v = 1.0 / 3.0
    ax.text(v, v, v, 'center', ha='center', va='center')


class TestScatter:
    @image_comparison(baseline_images=['scatter'], extensions=['pdf'],
                      tol=1.0, style='mpl20')
    def test_scatter(self):
        tn0, tn1, tn2 = get_scatter_points()
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.scatter(tn0, tn1, tn2)

    @image_comparison(baseline_images=['scatter_color'], extensions=['pdf'],
                      tol=1.0, style='mpl20')
    def test_scatter_color(self):
        fix_text_kerning_factor()

        tn0, tn1, tn2 = get_scatter_points()
        fig = plt.figure()
        fig.subplots_adjust(left=0.075, right=0.85)
        ax = fig.add_subplot(111, projection='ternary')
        sc = ax.scatter(tn0, tn1, tn2, c=range(len(tn0)))
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
        tn0, tn1, tn2 = get_triangular_grid()
        dtn0 = 1.0 / 3.0 - tn0
        dtn1 = 1.0 / 3.0 - tn1
        dtn2 = 1.0 / 3.0 - tn2
        fig = plt.figure()
        ax = fig.add_subplot(projection='ternary')
        ax.quiver(tn0, tn1, tn2, dtn0, dtn1, dtn2)

    @image_comparison(baseline_images=['quiver_color'], extensions=['pdf'],
                      tol=0.3, style='mpl20')
    def test_quiver_color(self):
        fix_text_kerning_factor()

        tn0, tn1, tn2 = get_triangular_grid()
        dtn0 = 1.0 / 3.0 - tn0
        dtn1 = 1.0 / 3.0 - tn1
        dtn2 = 1.0 / 3.0 - tn2
        length = np.sqrt(dtn0**2 + dtn1**2 + dtn2**2)
        fig = plt.figure()
        fig.subplots_adjust(left=0.075, right=0.85)
        ax = fig.add_subplot(projection='ternary')
        pc = ax.quiver(tn0, tn1, tn2, dtn0, dtn1, dtn2, length)
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


@check_figures_equal(extensions=('pdf',))
def test_grid_both(fig_test, fig_ref):
    """Test if `grid("both")` gives the expected result."""
    ax = fig_test.add_subplot(projection="ternary")
    ax.grid(axis="both")

    ax = fig_ref.add_subplot(projection="ternary")
    ax.grid(axis="t")
    ax.grid(axis="l")
    ax.grid(axis="r")


@image_comparison(baseline_images=['legend'], extensions=['pdf'],
                  tol=0.3, style='mpl20')
def test_legend():
    """Test if the legend is plotted correctly."""
    fig = plt.figure()
    ax = fig.add_subplot(projection='ternary')

    for seed in [1, 9, 6, 8]:
        ax.scatter(*get_scatter_points(11, seed=seed), alpha=0.5, label=seed)

    ax.legend()
