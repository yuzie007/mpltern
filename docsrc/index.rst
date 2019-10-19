#######
Mpltern
#######

.. _source code: https://github.com/yuzie007/mpltern
.. _Matplotlib: https://matplotlib.org
.. _seaborn: https://seaborn.pydata.org
.. _Jupyter: http://jupyter.org

Mpltern is a Python plotting library based on Matplotlib_ specifically designed
for `ternary plots <https://en.wikipedia.org/wiki/Ternary_plot>`_.
Mpltern is implemented as a new projection for Matplotlib, with introducing
e.g. new ``Transform`` classes for ternary plots.
The followings are the features of Mpltern when compared with other
ternary-plot libraties:

- Many things one expects essentially possible using Matplotlib can be done
  also in Mpltern, without e.g. ternary-to-Cartesian conversions on the user
  side
- For the same plotting styles, Mpltern offers the same or very similar method
  names as Matplotlib does; you do not need to learn many new commands in
  addition to those for Matplotlib
- Easy combination with normal Matplotlib plots
- Easy application of seaborn_ styles
- Working also in Matplotlib interactive modes inside e.g. Jupyter_ notebooks

At the same time, Mpltern manages many cumbersome things like the positioning
of tick markers, tick labels, and axis labels. This allows users e.g. faster
production of ternary plots with publication quality.

..
   .. raw:: html

      <div class="responsive_screenshots">
         <a href="tutorials/introductory/sample_plots.html">
            <div class="responsive_subfig">
            <img align="middle" src="_images/sphx_glr_spans_thumb.svg"
             border="0" alt="screenshots"/>
            </div>
      </div>
      <span class="clear_screenshots"></span>

Installation
============

The latest version of Mpltern is available from `GitHub <source code_>`_.

.. code-block::

   git clone https://github.com/yuzie007/mpltern.git

Installations via PyPI and Conda are also planned.

Examples
========

Various examples of Mpltern are found in the
:doc:`examples gallery <gallery/index>`.

Citing Mpltern
==============

At this moment, the author requests to cite the URL of this page if Mpltern
contributes to a scientific publication.
Of course, `Matplotlib should be also very much acknowledged <https://matplotlib.org/citing.html>`_
when using Mpltern.

DOIs
----

None yet.

Author
======

Yuji Ikeda (Max-Planck-Institut für Eisenforschung GmbH, Germany)
