"""
=========================
USDA soil texture classes
=========================
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from matplotlib._cm import _Set3_data
from mpltern.datasets import soil_texture_classes


def calculate_centroid(vertices):
    """Calculte the centroid of a polygon.

    https://en.wikipedia.org/wiki/Centroid#Of_a_polygon

    Parameters
    ----------
    vertices : (n, 2) np.ndarray
        Vertices of a polygon.

    Returns
    -------
    centroid : (2, ) np.ndarray
        Centroid of the polygon.
    """
    roll0 = np.roll(vertices, 0, axis=0)
    roll1 = np.roll(vertices, 1, axis=0)
    cross = np.cross(roll0, roll1)
    area = 0.5 * np.sum(cross)
    return np.sum((roll0 + roll1) * cross[:, None], axis=0) / (6.0 * area)


def plot_soil_texture_classes(ax):
    """Plot soil texture classes."""
    classes = soil_texture_classes

    for (key, value), color in zip(classes.items(), _Set3_data):
        tn0, tn1, tn2 = np.array(value).T
        patch = ax.fill(tn0, tn1, tn2, ec="k", fc=color, alpha=0.6, zorder=2.1)
        centroid = calculate_centroid(patch[0].get_xy())

        # last space replaced with line break
        label = key[::-1].replace(" ", "\n", 1)[::-1].capitalize()

        ax.text(
            centroid[0],
            centroid[1],
            label,
            ha="center",
            va="center",
            transform=ax.transData,
        )

    ax.taxis.set_major_locator(MultipleLocator(10.0))
    ax.laxis.set_major_locator(MultipleLocator(10.0))
    ax.raxis.set_major_locator(MultipleLocator(10.0))

    ax.taxis.set_minor_locator(AutoMinorLocator(2))
    ax.laxis.set_minor_locator(AutoMinorLocator(2))
    ax.raxis.set_minor_locator(AutoMinorLocator(2))

    ax.grid(which="both")

    ax.set_tlabel("Clay (%)")
    ax.set_llabel("Sand (%)")
    ax.set_rlabel("Silt (%)")

    ax.taxis.set_ticks_position("tick2")
    ax.laxis.set_ticks_position("tick2")
    ax.raxis.set_ticks_position("tick2")


def main():
    """Main"""
    ax = plt.subplot(projection="ternary", ternary_sum=100.0)
    plot_soil_texture_classes(ax)
    # add plot here on top of USDA soil texture classes with zorder of e.g. 2.5
    plt.show()


if __name__ == "__main__":
    main()
