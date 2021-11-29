from matplotlib.projections import register_projection
from mpltern.ternary import TernaryAxes

from ._version import version as __version__

register_projection(TernaryAxes)
