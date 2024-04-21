"""Tests for custom triangles."""
from itertools import product

import matplotlib.pyplot as plt
import pytest
from matplotlib.testing.decorators import image_comparison

from mpltern.datasets import get_spiral


class TestGivenTriangles:
    """Tests for custom triangles."""
    labelrotations = ["tick", "axis", "horizontal"]
    rotations = range(0, 360, 90)
    expected = [
        (lr, r, [f"given_triangles_{lr}_{r}"])
        for lr, r in product(labelrotations, rotations)
    ]

    @pytest.mark.parametrize(
        "labelrotation, rotation, baseline_images",
        expected,
    )
    @image_comparison(baseline_images=None, extensions=["pdf"], style="mpl20")
    def test_given_triangles(self, labelrotation, rotation, baseline_images):
        """Test custom triangles.

        Test if tick-markers, tick-labels, and axis-labels are shown as
        expected for custom triangles.
        """
        if "text.kerning_factor" in plt.rcParams:
            plt.rcParams["text.kerning_factor"] = 6

        corners = ((0.5, 0.0), (1.0, 0.5), (0.0, 1.0))
        ax = plt.subplot(
            projection="ternary",
            corners=corners,
            rotation=rotation,
        )
        tn0, tn1, tn2 = get_spiral()
        ax.plot(tn0, tn1, tn2)

        ax.set_tlabel("Top")
        ax.set_llabel("Left")
        ax.set_rlabel("Right")

        ax.tick_params(labelrotation=labelrotation)

        ax.grid()
