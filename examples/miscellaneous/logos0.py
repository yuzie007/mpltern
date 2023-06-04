"""
============
Mpltern logo
============

This example generates the current mpltern logo.
This is based on the `matplotlib logo
<https://matplotlib.org/stable/gallery/misc/logos2.html>`__.
The dark-mode logo is also obtained with ``MPL_BLUE = '#65baea'``.
"""
import matplotlib.pyplot as plt

import matplotlib.font_manager
from matplotlib.patches import PathPatch
from matplotlib.text import TextPath
import matplotlib.transforms as mtrans
import mpltern  # noqa: F401

MPL_BLUE = '#11557c'


def get_font_properties():
    return matplotlib.font_manager.FontProperties(weight='bold')


def create_icon_axes(fig, ax_position, lw_grid, lw_border):
    """
    Create a ternary axes containing the mpltern span plot.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to draw into.
    ax_position : (float, float, float, float)
        The position of the created Axes in figure coordinates as
        (x, y, width, height).
    lw_grid : float
        The linewidth of the grid.
    lw_border : float
        The linewidth of the Axes border.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The created Axes.
    """
    with plt.rc_context({'axes.edgecolor': MPL_BLUE,
                         'axes.linewidth': lw_border}):
        ax = fig.add_axes(ax_position, projection='ternary')

        ax.axtspan(0.4, 0.6, color='C0', alpha=0.6)
        ax.axlspan(0.4, 0.6, color='C1', alpha=0.6)
        ax.axrspan(0.4, 0.6, color='C2', alpha=0.6)

        ax.tick_params(
            tick1On=False, tick2On=False, label1On=False, label2On=False)

        ax.grid(lw=lw_grid, color='0.9')
        # the actual visible background - extends a bit beyond the axis
        ax.fill(
            (1.04, -0.02, -0.02),
            (-0.02, 1.04, -0.02),
            (-0.02, -0.02, 1.04),
            facecolor='white', zorder=0,
            clip_on=False, in_layout=False)
        return ax


def create_text_axes(fig, height_px):
    """Create an Axes in *fig* that contains 'mpltern' as Text."""
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_aspect("equal")
    ax.set_axis_off()

    path = TextPath((0, 0), "mpl  tern", size=height_px * 0.8,
                    prop=get_font_properties())

    angle = 4.25  # degrees
    trans = mtrans.Affine2D().skew_deg(angle, 0)

    patch = PathPatch(path, transform=trans + ax.transData, color=MPL_BLUE,
                      lw=0)
    ax.add_patch(patch)
    ax.autoscale()


def make_logo(height_px, lw_grid, lw_border, with_text=False):
    """
    Create a full figure with the mpltern logo.

    Parameters
    ----------
    height_px : int
        Height of the figure in pixel.
    lw_grid : float
        The linewidth of the grid.
    lw_border : float
        The linewidth of icon border.
    with_text : bool
        Whether to draw only the icon or to include 'mpltern' as text.
    """
    dpi = 100
    height = height_px / dpi
    figsize = (5 * height, height) if with_text else (height, height)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.patch.set_alpha(0)

    if with_text:
        create_text_axes(fig, height_px)

    ax_pos = (0.395, 0.12, .17, 0.75) if with_text else (0.1, 0.1, 0.8, 0.8)
    ax = create_icon_axes(fig, ax_pos, lw_grid, lw_border)

    return fig, ax


# %%
# A large logo:

make_logo(height_px=110, lw_grid=0.5, lw_border=1)

# %%
# A small 32px logo:

make_logo(height_px=32, lw_grid=0.3, lw_border=0.3)

# %%
# A large logo including text, as used on the mpltern website.

make_logo(height_px=110, lw_grid=0.5, lw_border=1,
          with_text=True)
plt.show()
