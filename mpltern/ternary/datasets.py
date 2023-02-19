import warnings

from mpltern.datasets import (get_dirichlet_pdfs, get_scatter_points,
                              get_shanon_entropies, get_spiral,
                              get_triangular_grid)

msg = "`mpltern.ternary.datasets.py` has been moved to `mpltern.datasets.py` "
msg += "and will be removed from the present directory in mpltern 0.6.0."
warnings.warn(msg)
