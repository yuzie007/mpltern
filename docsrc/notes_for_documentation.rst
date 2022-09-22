###############################
Notes for mpltern Documentation
###############################

This page is personal notes of the author and summarizes the things learned
about `Sphinx <https://www.sphinx-doc.org/en/master/>`_ and
`Read the Docs <https://docs.readthedocs.io/en/stable/>`_ during the
documentation of mpltern 0.3.1+.

How to redirect to Read the Docs
================================

The website https://yuzie007.github.io/mpltern is now redirected to
https://mpltern.readthedocs.io following the way in
https://gist.github.com/domenic/1f286d415559b56d725bee51a62c24a7.


How the table of contents displays
==================================

In Sphinx version 2.0+, the TOC taken from "contents" by default.
Read the Docs, in contrast, the home page, which is "index" by default, is
supposed to have ``toctree``, from which the TOC is created.
What I wanted to do is to set "index" as the home page without showing the TOC
explicitly. This can be actually achieved by following
https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html#how-the-table-of-contents-displays.
