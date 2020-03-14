from matplotlib.testing.conftest import *


@pytest.fixture
def mpltern_test_settings():
    # `text.kerning_factor` introduced since Matplotlib 3.2.0, changes default
    # text positions. To be compatible with baseline_images, the old behavior
    # is restored.
    if 'text.kerning_factor' in matplotlib.rcParams:
        matplotlib.rcParams['text.kerning_factor'] = 6
