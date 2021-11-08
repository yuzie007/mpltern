"""Tests for TernaryAxes3D"""
import matplotlib.pyplot as plt

import mpltern


def test_3d():
    """Test if TernaryAxes3D can be initialized."""
    plt.figure().add_subplot(projection='ternary3d')
