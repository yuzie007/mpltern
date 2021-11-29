from matplotlib.projections import register_projection
from mpltern.ternary import TernaryAxes

try:  # py38 or later
    from importlib.metadata import version, PackageNotFoundError
    try:
        __version__ = version("mpltern")
    except PackageNotFoundError:
        # package is not installed
        pass
except ImportError:  # py36, py37
    from pkg_resources import get_distribution, DistributionNotFound
    try:
        __version__ = get_distribution(__name__).version
    except DistributionNotFound:
        # package is not installed
        pass

register_projection(TernaryAxes)
