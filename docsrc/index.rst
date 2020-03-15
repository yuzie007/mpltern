######################################
mpltern: Ternary plots with Matplotlib
######################################

.. title:: mpltern

.. _Matplotlib: https://matplotlib.org
.. _seaborn: https://seaborn.pydata.org
.. _Jupyter: http://jupyter.org

Mpltern is a Python plotting library based on Matplotlib_ specifically designed
for `ternary plots <https://en.wikipedia.org/wiki/Ternary_plot>`_.
Mpltern is implemented as a new projection for Matplotlib, with introducing
e.g. new ``Transform`` classes for ternary plots.
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
- Easy application of seaborn_ styles
- Working also in Matplotlib interactive modes inside e.g. Jupyter_ notebooks

.. raw:: html

   <div class="responsive_screenshots">
      <a href="gallery/index.html">
         <div class="responsive_subfig">
         <img align="middle" src="_images/sphx_glr_with_seaborn_styles_001.svg"
          border="0" alt="screenshots"/>
         </div>
         <div class="responsive_subfig">
         <img align="middle" src="_images/sphx_glr_05.inset_001.svg"
          border="0" alt="screenshots"/>
         </div>
         <div class="responsive_subfig">
         <img align="middle" src="_images/basic_2.svg"
          border="0" alt="screenshots"/>
         </div>
         <div class="responsive_subfig">
         <img align="middle" src="_images/sphx_glr_02.arbitrary_triangle_001.svg"
          border="0" alt="screenshots"/>
         </div>
      </a>
   </div>
   <span class="clear_screenshots"></span>

Citing mpltern
==============

The author requests to cite mpltern via the DOIs below if mpltern contributes
to a scientific publication.
Of course, `Matplotlib should be also very much acknowledged <https://matplotlib.org/citing.html>`_
when using mpltern.

DOIs
----
0.3.0
   .. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3528355.svg
      :target: https://doi.org/10.5281/zenodo.3528355

Author
======

Yuji Ikeda
(`Github <https://github.com/yuzie007>`_,
`Google Scholar <https://scholar.google.co.jp/citations?user=2m5dkBwAAAAJ&hl=en>`_,
`ResearchGate <https://www.researchgate.net/profile/Yuji_Ikeda6>`_)

.. toctree::
   :hidden:
   :maxdepth: 2

   supported_matplotlib.rst
   installation.rst
   basic_usage.rst
   implemented_methods.rst
   gallery/index.rst
   conventions.rst
   aims.rst
   publications.rst
   alternatives.rst
   notes_for_implementation.rst
   notes_for_documentation.rst
   TODO.rst
