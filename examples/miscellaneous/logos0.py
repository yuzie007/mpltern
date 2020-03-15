"""
====
Logo
====

This example generates the current mpltern logo.
"""
import matplotlib.pyplot as plt
import mpltern  # noqa: F401


def create_icon_axes(fig, ax_position, lw_border):
    """
    Create a ternary axes containing the mpltern span plot.

    Parameters
    ----------
    fig : matplotlib.figure.Figure
        The figure to draw into.
    ax_position : (float, float, float, float)
        The position of the created Axes in figure coordinates as
        (x, y, width, height).
    lw_border : float
        The linewidth of the Axes border.

    Returns
    -------
    ax : matplotlib.axes.Axes
        The created Axes.
    """
    with plt.rc_context({'axes.linewidth': lw_border}):
        ax = fig.add_axes(ax_position, projection='ternary')
        ax.tick_params(
            tick1On=False, tick2On=False, label1On=False, label2On=False)

        ax.axtline(0.5, lw=lw_border, color='C0')
        ax.axlline(0.5, lw=lw_border, color='C1')
        ax.axrline(0.5, lw=lw_border, color='C2')
        ax.axtspan(0.4, 0.6, color='C0', alpha=0.2)
        ax.axlspan(0.4, 0.6, color='C1', alpha=0.2)
        ax.axrspan(0.4, 0.6, color='C2', alpha=0.2)

        return ax


def add_mpltern_text(ax):
    ax.text(0.995, 0.5, "mpltern", fontsize=128,
            ha='right', va='center', alpha=1.0, transform=ax.transAxes)


def make_logo(height_px, lw_border, with_text=False):
    """
    Create a full figure with the mpltern logo.

    Parameters
    ----------
    height_px : int
        Height of the figure in pixel.
    lw_border : float
        The linewidth of icon border.
    with_text : bool
        Whether to draw only the icon or to include 'mpltern' as text.
    """
    dpi = 72
    height = height_px / dpi
    figsize = (5.0 * height, height) if with_text else (height, height)
    fig = plt.figure(figsize=figsize, dpi=dpi)
    fig.patch.set_alpha(0)

    if with_text:
        ax = fig.add_axes([0., 0., 1., 1.])
        add_mpltern_text(ax)
        ax.axis('off')

    ax_pos = (0.02, 0.075, 0.2, 0.85) if with_text else (0.1, 0.1, 0.8, 0.8)
    ax = create_icon_axes(fig, ax_pos, lw_border)

    return fig, ax


##############################################################################
# A large logo:

make_logo(height_px=128, lw_border=3)

##############################################################################
# A large logo including text, as used on the mpltern website.

make_logo(height_px=128, lw_border=3, with_text=True)

plt.show()
