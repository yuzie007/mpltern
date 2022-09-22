###############
Aims of mpltern
###############

Compared with other Python-based implementations for ternary plots,
mpltern focuses on providing a similar user experience to Matplotlib.
Practically, this aim is hopefully accomplished by:

- Implementation of ``TernaryAxes`` inheriting ``Axes`` of Matplotlib.
    - Components of ``Axes`` like ``Axis`` and ``Tick`` are also overridden as
      ``TernaryAxis`` and ``TernaryTick``, respectively.
- Parameters in ``rcParams`` of Matplotlib rather than hard-coded defaults.
  This also enables us to use seaborn styles with mpltern.
- Employments of new ``transform`` classes useful for ternary plots.
  This particularly makes mpltern work nicely not only in non-interactive modes
  but also in interactive modes.

