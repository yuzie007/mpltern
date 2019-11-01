from matplotlib.projections import register_projection
from mpltern.ternary import TernaryAxes

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

register_projection(TernaryAxes)
