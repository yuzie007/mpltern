from matplotlib.projections import register_projection
from .ternary import TernaryAxes
__version__ = '0.2.0'
register_projection(TernaryAxes)
