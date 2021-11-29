# mpltern

[![PyPI version](https://badge.fury.io/py/mpltern.svg)](https://badge.fury.io/py/mpltern)
[![PyPI](https://img.shields.io/pypi/dm/mpltern.svg)](https://pypi.python.org/pypi/mpltern)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/mpltern.svg)](https://anaconda.org/conda-forge/mpltern)
[![Conda Downloads](https://img.shields.io/conda/dn/conda-forge/mpltern.svg)](https://anaconda.org/conda-forge/mpltern)

[![GitHubActions](https://github.com/yuzie007/mpltern/actions/workflows/tests.yml/badge.svg)](https://github.com/yuzie007/mpltern/actions?query=workflow%3ATests)
[![CircleCI](https://circleci.com/gh/yuzie007/mpltern.svg?style=shield)](https://circleci.com/gh/yuzie007/mpltern)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3528355.svg)](https://doi.org/10.5281/zenodo.3528355)

Mpltern is a Python plotting library based on
[Matplotlib](https://matplotlib.org), specifically designed for
[ternary plots](https://en.wikipedia.org/wiki/Ternary_plot).
Mpltern is implemented as a new projection for Matplotlib, with introducing
e.g. new `Transform` classes for ternary plots.
The followings are the features of mpltern when compared with other
ternary-plot libraries:

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

[<img src="https://mpltern.readthedocs.io/en/latest/_images/sphx_glr_with_seaborn_styles_001.svg" width="162"/>](https://yuzie007.github.io/mpltern/gallery/index.html)
[<img src="https://mpltern.readthedocs.io/en/latest/_images/sphx_glr_05.inset_001.svg" width="162"/>](https://yuzie007.github.io/mpltern/gallery/index.html)
[<img src="https://mpltern.readthedocs.io/en/latest/_images/basic_2.svg" width="162"/>](https://yuzie007.github.io/mpltern/gallery/index.html)
[<img src="https://mpltern.readthedocs.io/en/latest/_images/sphx_glr_02.arbitrary_triangle_001.svg" width="162"/>](https://yuzie007.github.io/mpltern/gallery/index.html)

## Author

Yuji Ikeda
([Github](https://github.com/yuzie007),
[Google Scholar](https://scholar.google.com/citations?user=2m5dkBwAAAAJ&hl=en),
[ResearchGate](https://www.researchgate.net/profile/Yuji_Ikeda6))
