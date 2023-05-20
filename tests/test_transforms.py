"""Test transforms for ternary plots."""
import numpy as np
import pytest

from mpltern.ternary.transforms import (BarycentricTransform,
                                        PSTransform,
                                        PCTransform,
                                        TernaryTransform)

corners_list = [
    ((0.5, 0.0), (1.0, 0.5), (0.0, 1.0)),
    ((0.0, 0.0), (1.0, 0.0), (0.5, 1.0)),
]


@pytest.mark.parametrize("corners", corners_list)
@pytest.mark.parametrize("index", [0, 1, 2])
def test_ternary_transform(corners, index):
    """Test TernaryTransform."""
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 2)
    points /= np.sum(points, axis=1)[:, None]

    trans = TernaryTransform(corners, index)
    points_transformed = trans.transform(points)
    points_inverted = trans.inverted().transform(points_transformed)

    np.testing.assert_almost_equal(points_inverted, points)


@pytest.mark.parametrize("corners", corners_list)
@pytest.mark.parametrize("index", [0, 1, 2])
def test_ternary_perpendicular_transform(corners, index):
    """Test TernaryPerpendicularTransform."""
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 2)
    points /= np.sum(points, axis=1)[:, None]

    trans = PSTransform(TernaryTransform(corners, index))
    points_transformed = trans.transform(points)
    points_inverted = trans.inverted().transform(points_transformed)

    np.testing.assert_almost_equal(points_inverted, points)


@pytest.mark.parametrize("corners", corners_list)
@pytest.mark.parametrize("index", [0, 1, 2])
def test_perpendicular_1_transform(corners, index):
    """Test TernaryPerpendicularTransform."""
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 2)
    points /= np.sum(points, axis=1)[:, None]

    trans = PCTransform(TernaryTransform(corners, index))
    points_transformed = trans.transform(points)
    points_inverted = trans.inverted().transform(points_transformed)

    np.testing.assert_almost_equal(points_inverted, points)


@pytest.mark.parametrize("scale", [1.0, 2.0, -1.0, -2.0])
@pytest.mark.parametrize("corners", corners_list)
def test_barycentric_transform(scale, corners):
    """Test BarycentricTransform."""
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 3)
    points *= scale / np.sum(points, axis=1)[:, None]

    trans = BarycentricTransform(corners)
    points_transformed = trans.transform(points)
    points_inverted = trans.inverted().transform(points_transformed)

    np.testing.assert_almost_equal(points_inverted, points)
