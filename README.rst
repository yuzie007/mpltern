######################################
mpltern: Ternary plots with Matplotlib
######################################

.. title:: mpltern

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
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3528355.svg
   :target: https://doi.org/10.5281/zenodo.3528355

|PyPI version| |PyPI| |Conda Version| |Conda Downloads|

|GitHubActions| |CircleCI|

|DOI|

Mpltern (https://yuzie007.github.io/mpltern) is a Python plotting library based
on `Matplotlib <https://matplotlib.org>`__ specifically designed
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
- Easy application of `seaborn <https://seaborn.pydata.org>`__ styles
- Working also in Matplotlib interactive modes inside e.g.
  `Jupyter <http://jupyter.org>`__ notebooks

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

Installation
============

PyPI
----

The latest released version is available from `PyPI <https://pypi.org/project/mpltern>`__.

.. code-block:: console

   python -m pip install -U mpltern

Conda
-----

The latest released version is available from `conda-forge <https://anaconda.org/conda-forge/mpltern>`__.

.. code-block:: console

   conda config --add channels conda-forge
   conda install mpltern

GitHub
------

The development version is available from `GitHub <https://github.com/yuzie007/mpltern>`__.

.. code-block:: console

   python -m pip install -U git+https://github.com/yuzie007/mpltern.git

Basic Usage
===========

Import mpltern as well as Matplotlib as:

.. code-block:: python

    import matplotlib.pyplot as plt
    import mpltern

By ``import mpltern``, a Matplotlib projection ``'ternary'`` is
registered inside.

Then, make ``TernaryAxes`` e.g. as:

.. code-block:: python

    ax = plt.subplot(projection='ternary')

It is already possible to create ternary plots using the methods in ``ax``.
For example:

.. code-block:: python

    from mpltern.ternary.datasets import get_spiral

    t, l, r = mpltern.datasets.get_spiral()
    # t: [0.33333333 0.33357906 0.33430414 ...]
    # l: [0.33333333 0.33455407 0.33543547 ...]
    # r: [0.33333333 0.33186687 0.33026039 ...]
    ax.plot(t, l, r)
    plt.show()

You may see the following Archimedean spiral in the triangle.

.. image:: https://mpltern.readthedocs.io/en/latest/_images/basic_1.svg

Contour-like plots are also possible in mpltern.

.. code-block:: python

    ax = plt.subplot(projection='ternary')

    from mpltern.ternary.datasets import get_shanon_entropies

    t, l, r, v = get_shanon_entropies()
    # t: [ 0. 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.1 0.1 0.1 ...]
    # l: [ 0. 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.  0.  0.1 0.2 ...]
    # r: [ 1. 0.9 0.8 0.7 0.6 0.5 0.4 0.3 0.2 0.1 0.  0.9 0.8 0.7 ...]
    # v: [-0. 0.32508297  0.50040242  ...]
    ax.tricontourf(t, l, r, v)
    plt.show()

.. image:: https://mpltern.readthedocs.io/en/latest/_images/basic_2.svg

See `more examples <https://mpltern.readthedocs.io/en/latest/gallery/index.html>`__.

How to Cite mpltern
===================

The author requests to cite mpltern via the DOI above if mpltern contributes
to a scientific publication.
Of course, `Matplotlib should be also very much acknowledged <https://matplotlib.org/citing.html>`_
when using mpltern.

Author
======

Yuji Ikeda
(`Github <https://github.com/yuzie007>`__,
`Google Scholar <https://scholar.google.co.jp/citations?user=2m5dkBwAAAAJ&hl=en>`__,
`ResearchGate <https://www.researchgate.net/profile/Yuji_Ikeda6>`__)
