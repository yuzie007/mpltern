######################################
mpltern: Ternary plots with Matplotlib
######################################

.. title:: mpltern

.. _Matplotlib: https://matplotlib.org
.. _seaborn: https://seaborn.pydata.org
.. _Jupyter: http://jupyter.org

.. |PyPI version| image:: https://badge.fury.io/py/mpltern.svg
   :target: https://badge.fury.io/py/mpltern
.. |PyPI| image:: https://img.shields.io/pypi/dm/mpltern.svg
   :target: https://pypi.python.org/pypi/mpltern
.. |Conda Version| image:: https://img.shields.io/conda/vn/conda-forge/mpltern.svg
   :target: https://anaconda.org/conda-forge/mpltern
.. |Conda Downloads| image:: https://img.shields.io/conda/dn/conda-forge/mpltern.svg
   :target: https://anaconda.org/conda-forge/mpltern
.. |GitHubActions| image:: https://github.com/yuzie007/mpltern/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/yuzie007/mpltern/actions?query=workflow%3ATests
.. |CircleCI| image:: https://circleci.com/gh/yuzie007/mpltern.svg?style=shield
   :target: https://circleci.com/gh/yuzie007/mpltern

|PyPI version| |PyPI| |Conda Version| |Conda Downloads|

|GitHubActions| |CircleCI|

Mpltern is a Python plotting library based on Matplotlib_ specifically designed
for `ternary plots <https://en.wikipedia.org/wiki/Ternary_plot>`_.
Mpltern is implemented as a new projection for Matplotlib, with introducing
e.g. new ``Transform`` classes for ternary plots.
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
- Easy application of seaborn_ styles
- Working also in Matplotlib interactive modes inside e.g. Jupyter_ notebooks

Details of mpltern are found in https://yuzie007.github.io/mpltern.

.. rst-class:: special

.. list-table::
   :widths: auto

   * - .. image:: https://mpltern.readthedocs.io/en/latest/_images/sphx_glr_with_seaborn_styles_001.svg
          :target: https://mpltern.readthedocs.io/en/latest/gallery/index.html
     - .. image:: https://mpltern.readthedocs.io/en/latest/_images/sphx_glr_05.inset_001.svg
          :target: https://mpltern.readthedocs.io/en/latest/gallery/index.html
     - .. image:: https://mpltern.readthedocs.io/en/latest/_images/basic_2.svg
          :target: https://mpltern.readthedocs.io/en/latest/gallery/index.html
     - .. image:: https://mpltern.readthedocs.io/en/latest/_images/sphx_glr_02.arbitrary_triangle_001.svg
          :target: https://mpltern.readthedocs.io/en/latest/gallery/index.html

Citing mpltern
==============

The author requests to cite mpltern via the DOIs below if mpltern contributes
to a scientific publication.
Of course, `Matplotlib should be also very much acknowledged <https://matplotlib.org/citing.html>`_
when using mpltern.

DOIs
----

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3528354.svg
   :target: https://doi.org/10.5281/zenodo.3528354

Author
======

Yuji Ikeda
(`Github <https://github.com/yuzie007>`_,
`Google Scholar <https://scholar.google.co.jp/citations?user=2m5dkBwAAAAJ&hl=en>`_,
`ResearchGate <https://www.researchgate.net/profile/Yuji_Ikeda6>`_)
