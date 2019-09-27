import numpy as np
import pytest
from taxes.transforms import TernaryDataTransform, BarycentricTransform


corners_list = [
    ((0.5, 0.0), (1.0, 0.5), (0.0, 1.0)),
    ((0.0, 0.0), (1.0, 0.0), (0.5, 1.0)),
]

@pytest.mark.parametrize('scale', [1.0, 2.0, -1.0, -2.0])
@pytest.mark.parametrize('corners', corners_list)
def test_ternary_data_transform(scale, corners):
    np.random.seed(19860107)
    points = np.random.rand(300).reshape(-1, 3)
    points *= (scale / np.sum(points, axis=1)[:, None])
    # print(points)

    trans = TernaryDataTransform(scale, corners)

    points_transformed = trans.transform(points)
    # print(points_transformed)

    np.testing.assert_almost_equal(
        points, trans.inverted().transform(points_transformed))


@pytest.mark.parametrize('scale', [1.0, 2.0, -1.0, -2.0])
@pytest.mark.parametrize('corners', corners_list)
def test_barycentric_transform(scale, corners):
    np.random.seed(1986)
    points = np.random.rand(300).reshape(-1, 3)
    points *= (scale / np.sum(points, axis=1)[:, None])
    # print(points)

    trans = BarycentricTransform(corners)

    points_transformed = trans.transform(points)
    # print(points_transformed)

    np.testing.assert_almost_equal(
        points, trans.inverted().transform(points_transformed))
