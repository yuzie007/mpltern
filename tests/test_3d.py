"""Tests for TernaryAxes3D"""
import matplotlib.pyplot as plt

from mpltern.datasets import get_shanon_entropies, get_spiral


def test_plot():
    """Test if `plot` works as expected."""
    ax = plt.figure().add_subplot(projection='ternary3d')
    ax.plot(*get_spiral(), zs=0.0)


def test_plot_trisurf():
    """Test if `plot_trisurf` works as expected."""
    ax = plt.figure().add_subplot(projection='ternary3d')
    tn0, tn1, tn2, entropies = get_shanon_entropies()
    ax.plot_trisurf(tn0, tn1, tn2, entropies)


def test_tricontour():
    """Test if `tricontour` works as expected."""
    ax = plt.figure().add_subplot(projection='ternary3d')
    tn0, tn1, tn2, entropies = get_shanon_entropies()
    ax.tricontour(tn0, tn1, tn2, entropies)


def test_tricontourf():
    """Test if `tricontourf` works as expected."""
    ax = plt.figure().add_subplot(projection='ternary3d')
    tn0, tn1, tn2, entropies = get_shanon_entropies()
    ax.tricontourf(tn0, tn1, tn2, entropies)


def test_scatter():
    """Test if `scatter` works as expected."""
    ax = plt.figure().add_subplot(projection='ternary3d')
    tn0, tn1, tn2, entropies = get_shanon_entropies()
    ax.scatter(tn0, tn1, tn2, entropies)
