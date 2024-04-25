mpltern 1.0.4 (2024-04-xx)
==========================

**Matplotlib 3.4.0-3.8.x**

What's new
----------

Interactive plots broken in mpltern 1.0.3 for `ternary_sum != 1.0` is fixed.

Ternary values in `hexbin` and `tribin` are now cast into float inside before
normalization (https://github.com/yuzie007/mpltern/issues/15).
