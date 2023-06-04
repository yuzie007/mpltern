import matplotlib.pyplot as plt
import mpltern
import pytest
from mpltern.ternary.spines import Spine


def test_invalid_spine():
    """Test if `Spine` raises `ValueError` for an invalid spine name."""
    fig = plt.figure()
    ax = fig.add_subplot(projection="ternary")
    with pytest.raises(ValueError):
        Spine.linear_spine(ax, "")
