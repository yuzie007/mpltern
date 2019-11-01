# mpltern

[![Build Status](https://travis-ci.org/yuzie007/mpltern.svg?branch=master)](https://travis-ci.org/yuzie007/mpltern)

Mpltern is a Python plotting library based on
[Matplotlib](https://matplotlib.org), specifically designed for
[ternary plots](https://en.wikipedia.org/wiki/Ternary_plot).
Mpltern is implemented as a new projection for Matplotlib, with introducing
e.g. new `Transform` classes for ternary plots.
The followings are the features of mpltern when compared with other
ternary-plot libraties:

- Many things one expects essentially possible using Matplotlib can be done
  also in mpltern, without e.g. ternary-to-Cartesian conversions on the user
  side
- For the same plotting styles, mpltern offers the same or very similar method
  names as Matplotlib does; you do not need to learn many new commands in
  addition to those for Matplotlib
- Tick markers, tick labels, and axis labels are automatically positioned with
  reasonable paddings inherited from Matplotlib;
  this allows users e.g. faster production of ternary plots with publication
  quality
- Easy combination with normal Matplotlib plots
- Easy application of [seaborn](https://seaborn.pydata.org) styles
- Working also in Matplotlib interactive modes inside e.g.
  [Jupyter](http://jupyter.org) notebooks

Details of mpltern are found in https://yuzie007.github.io/mpltern.

## Author

Yuji Ikeda
([Github](https://github.com/yuzie007),
[Google Scholar](https://scholar.google.com/citations?user=2m5dkBwAAAAJ&hl=en),
[ResearchGate](https://www.researchgate.net/profile/Yuji_Ikeda6))
