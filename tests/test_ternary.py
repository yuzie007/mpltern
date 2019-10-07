from matplotlib.testing.decorators import (
    image_comparison, check_figures_equal)
import matplotlib.pyplot as plt
from taxes.datasets import get_spiral


@image_comparison(baseline_images=['axis_and_tick'], style='mpl20')
def test_axis_and_tick():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='ternary')

    ax.set_tlabel('Top')
    ax.set_llabel('Left')
    ax.set_rlabel('Right')

    ax.taxis.set_label_position('bottom')
    ax.laxis.set_label_position('bottom')
    ax.raxis.set_label_position('bottom')

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


@image_comparison(baseline_images=['given_triangles'], style='mpl20')
def test_given_triangles():
    # Check if the tick-markers, tick-labels, and axis-labels are shown as
    # expected.
    fig = plt.figure()
    corners = ((0.5, 0.0), (1.0, 0.5), (0.0, 1.0))
    ax = fig.add_subplot(111, corners=corners, projection='ternary')
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