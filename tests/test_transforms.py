"""Test transforms for ternary plots."""
import numpy as np
import pytest

from matplotlib.transforms import Bbox, IdentityTransform
from mpltern.ternary.transforms import (BarycentricTransform,
                                        T2HHeightTransform,
                                        T2HWidthTransform,
                                        TernaryAxisLabelSTransform,
                                        TernaryAxisLabelCTransform,
                                        TernaryAxisTransform)

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

    trans = TernaryAxisTransform(corners, index)
    points_transformed = trans.transform(points)
    points_inverted = trans.inverted().transform(points_transformed)

    np.testing.assert_almost_equal(points_inverted, points)


@pytest.mark.parametrize("corners", corners_list)
@pytest.mark.parametrize("index", [0, 1, 2])
def test_label_s_transform(corners, index):
    """Test TernaryPerpendicularTransform."""
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 2)
    points /= np.sum(points, axis=1)[:, None]

    trans = TernaryAxisLabelSTransform(TernaryAxisTransform(corners, index), IdentityTransform())
    points_transformed = trans.transform(points)
    points_inverted = trans.inverted().transform(points_transformed)

    np.testing.assert_almost_equal(points_inverted, points)


@pytest.mark.parametrize("corners", corners_list)
@pytest.mark.parametrize("index", [0, 1, 2])
def test_label_c_transform(corners, index):
    """Test TernaryPerpendicularTransform."""
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 2)
    points /= np.sum(points, axis=1)[:, None]

    trans = TernaryAxisLabelCTransform(TernaryAxisTransform(corners, index), IdentityTransform())
    points_transformed = trans.transform(points)
    points_inverted = trans.inverted().transform(points_transformed)

    np.testing.assert_almost_equal(points_inverted, points)


@pytest.mark.parametrize("scale", [1.0, 2.0, -1.0, -2.0])
@pytest.mark.parametrize("index", [0, 1, 2])
def test_t2h_height_transform(scale, index):
    """Test T2HTransform."""
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 2)

    viewTLim = Bbox.unit()
    viewLLim = Bbox.unit()
    viewRLim = Bbox.unit()

    viewTLim.intervalx = 0.1, 0.9
    viewLLim.intervalx = 0.2, 0.8
    viewRLim.intervalx = 0.3, 0.7

    trans = T2HHeightTransform(scale, [viewTLim, viewLLim, viewRLim], index)
    points_transformed = trans.transform(points)
    points_inverted = trans.inverted().transform(points_transformed)

    np.testing.assert_almost_equal(points_inverted, points)


@pytest.mark.parametrize("scale", [1.0, 2.0, -1.0, -2.0])
@pytest.mark.parametrize("index", [0, 1, 2])
def test_t2h_width_transform(scale, index):
    """Test T2HTransform."""
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 2)

    viewTLim = Bbox.unit()
    viewLLim = Bbox.unit()
    viewRLim = Bbox.unit()

    viewTLim.intervalx = 0.1, 0.9
    viewLLim.intervalx = 0.2, 0.8
    viewRLim.intervalx = 0.3, 0.7

    trans = T2HWidthTransform(scale, [viewTLim, viewLLim, viewRLim], index)
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
