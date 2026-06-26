import matplotlib as mpl

mpl_version = tuple(int(_) for _ in mpl.__version__.split('.'))
tol = 12.0 if mpl_version >= (3, 11) else 0.0
