"""Tests for TernaryAxes3D"""
import matplotlib.pyplot as plt

import mpltern


def test_plot():
    """Test if `plot` works as expected."""
    ax = plt.figure().add_subplot(projection='ternary3d')
    ax.plot([1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0], zs=0.0)
