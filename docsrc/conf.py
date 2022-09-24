# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import shutil

from sphinx.transforms import SphinxTransform

import mpltern


# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx_gallery.gen_gallery',
    'sphinx_copybutton',
]


def _check_dependencies():
    names = {
        "colorspacious": 'colorspacious',
        "IPython.sphinxext.ipython_console_highlighting": 'ipython',
        "matplotlib": 'matplotlib',
        "numpydoc": 'numpydoc',
        "sphinx_copybutton": 'sphinx_copybutton',
        "sphinx_gallery": 'sphinx_gallery',
    }
    missing = []
    for name in names:
        try:
            __import__(name)
        except ImportError:
            missing.append(names[name])
    if missing:
        raise ImportError(
            "The following dependencies are missing to build the "
            "documentation: {}".format(", ".join(missing)))
    if shutil.which('dot') is None:
        raise OSError(
            "No binary named dot - graphviz must be installed to build the "
            "documentation")


_check_dependencies()


# On Linux, prevent plt.show() from emitting a non-GUI backend warning.
os.environ.pop("DISPLAY", None)

from sphinx_gallery.scrapers import matplotlib_scraper


class matplotlib_svg_scraper(object):
    # To make the figures in the SVG format
    # https://sphinx-gallery.github.io/advanced.html#id9

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return matplotlib_scraper(*args, format='svg', **kwargs)


# Sphinx gallery configuration
from sphinx_gallery.sorting import ExplicitOrder
from sphinx_gallery.sorting import FileNameSortKey
sphinx_gallery_conf = {
    'examples_dirs': ['../examples'],
    'filename_pattern': '^((?!sgskip).)*$',
    'gallery_dirs': ['gallery'],
    'doc_module': ('mpltern', ),
    'subsection_order': ExplicitOrder(['../examples/introductory',
                                       '../examples/intermediate',
                                       '../examples/axis_and_tick',
                                       '../examples/triangle',
                                       '../examples/advanced',
                                       '../examples/miscellaneous']),
    'within_subsection_order': FileNameSortKey,
    'min_reported_time': 1,
    # The following is commented out because SVG does not work nicely yet
    # for `ax.pcolormesh(shading='gouraud')
    'image_scrapers': (matplotlib_svg_scraper(),),
}

plot_gallery = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# This is the default encoding, but it doesn't hurt to be explicit
source_encoding = "utf-8"

# The master toctree document.
master_doc = 'index'  # default: 'contents'

project = 'mpltern'
copyright = '2019-2022, Yuji Ikeda'
author = 'Yuji Ikeda'

version = mpltern.__version__
# The full version, including alpha/beta/rc tags.
release = version

# Plot directive configuration
# ----------------------------

plot_formats = [('png', 100), ('pdf', 100)]

# GitHub extension

github_project_url = "https://github.com/yuzie007/mpltern/"

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# https://stackoverflow.com/a/52998585
class ReplaceMyBase(SphinxTransform):

    default_priority = 750
    prefix = "https://mpltern.readthedocs.io/en/latest/"

    def apply(self):
        from docutils.nodes import reference, Text
        basetext = lambda o: (
            isinstance(o, Text) and o.startswith(self.prefix))

        baseref = lambda o: (
            isinstance(o, reference) and
            o.get('uri', '').startswith(self.prefix))
        for node in self.document.traverse(baseref):
            target = node['uri'].replace(self.prefix, '', 1)
            node.replace_attr('uri', target)
            for t in node.traverse(basetext):
                t1 = Text(t.replace(self.prefix, '', 1), t.rawsource)
                t.parent.replace(t, t1)

        baseref = lambda o: (
            isinstance(o, reference) and
            o.get('refuri', '').startswith(self.prefix))
        for node in self.document.traverse(baseref):
            target = node['refuri'].replace(self.prefix, '', 1)
            node.replace_attr('refuri', target)
            for t in node.traverse(basetext):
                t1 = Text(t.replace(self.prefix, '', 1), t.rawsource)
                t.parent.replace(t, t1)
        return


def setup(app):
    # app.add_css_file("screenshots.css")
    app.add_transform(ReplaceMyBase)


# Path to favicon
html_favicon = '_static/favicon.ico'

html_logo = '_static/sphx_glr_logos0_002.svg'

# Workaround to remove matplotlib warning based on
# https://github.com/sphinx-gallery/sphinx-gallery/pull/521


import warnings

# Remove matplotlib agg warnings from generated doc when using plt.show
warnings.filterwarnings("ignore", category=UserWarning,
                        message='Matplotlib is currently using agg, which is a'
                                ' non-GUI backend, so cannot show the figure.')
