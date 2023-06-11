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
import sys
import warnings

sys.path.insert(0, os.path.abspath(".."))

import mpltern

from datetime import datetime
import time

from sphinx.transforms import SphinxTransform

# Parse year using SOURCE_DATE_EPOCH, falling back to current time.
# https://reproducible-builds.org/specs/source-date-epoch/
sourceyear = datetime.utcfromtimestamp(
    int(os.environ.get('SOURCE_DATE_EPOCH', time.time()))).year


# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'IPython.sphinxext.ipython_console_highlighting',
    'numpydoc',  # Needs to be loaded *after* autodoc.
    'sphinx_gallery.gen_gallery',
    'matplotlib.sphinxext.plot_directive',
    'sphinxext.custom_roles',
    'sphinx_copybutton',
]


def _check_dependencies():
    names = {
        **{ext: ext.split(".")[0] for ext in extensions},
        # Explicitly list deps that are not extensions, or whose PyPI package
        # name does not match the (toplevel) module name.
        "colorspacious": 'colorspacious',
        "pydata_sphinx_theme": 'pydata_sphinx_theme',
        "matplotlib": 'matplotlib',
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
            f"documentation: {', '.join(missing)}")
    if shutil.which('dot') is None:
        raise OSError(
            "No binary named dot - graphviz must be installed to build the "
            "documentation")

_check_dependencies()


# On Linux, prevent plt.show() from emitting a non-GUI backend warning.
os.environ.pop("DISPLAY", None)

intersphinx_mapping = {
    'matplotlib': ('https://matplotlib.org/stable/', None),
}


# Sphinx gallery configuration

from sphinx_gallery.scrapers import matplotlib_scraper


class matplotlib_svg_scraper(object):
    # To make the figures in the SVG format
    # https://sphinx-gallery.github.io/advanced.html#id9

    def __repr__(self):
        return self.__class__.__name__

    def __call__(self, *args, **kwargs):
        return matplotlib_scraper(*args, format='svg', **kwargs)


from sphinx_gallery.sorting import ExplicitOrder
from sphinx_gallery.sorting import FileNameSortKey

gallery_dirs = ['gallery']

example_dirs = ['../examples']
sphinx_gallery_conf = {
    'doc_module': ('mpltern', ),
    'examples_dirs': example_dirs,
    'filename_pattern': '^((?!sgskip).)*$',
    'gallery_dirs': gallery_dirs,
    # The following is commented out because SVG does not work nicely yet
    # for `ax.pcolormesh(shading='gouraud')
    'image_scrapers': (matplotlib_svg_scraper(),),
    'subsection_order': ExplicitOrder(['../examples/introductory',
                                       '../examples/intermediate',
                                       '../examples/statistics',
                                       '../examples/axis_and_tick',
                                       '../examples/limits',
                                       '../examples/transforms',
                                       '../examples/triangle',
                                       '../examples/miscellaneous']),
    'min_reported_time': 1,
    'plot_gallery': 'True',  # sphinx-gallery/913
    'within_subsection_order': FileNameSortKey,
    'capture_repr': (),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# This is the default encoding, but it doesn't hurt to be explicit
source_encoding = "utf-8"

# The toplevel toctree document (renamed to root_doc in Sphinx 4.0)
root_doc = master_doc = 'index'

project = 'mpltern'
copyright = (
    f'2019-{sourceyear} Yuji Ikeda'
)
author = 'Yuji Ikeda'


# The default replacements for |version| and |release|, also used in various
# other places throughout the built documents.
#
# The short X.Y version.

version = mpltern.__version__
# The full version, including alpha/beta/rc tags.
release = version

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

default_role = 'obj'

# Plot directive configuration
# ----------------------------

# https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html
plot_include_source = True
plot_html_show_source_link = False
plot_formats = ['svg']
plot_html_show_formats = False

# GitHub extension

github_project_url = "https://github.com/yuzie007/mpltern/"


# Options for HTML output
# -----------------------

# The style sheet to use for HTML and HTML Help pages. A file of that name
# must exist either in Sphinx' static/ path, or in one of the custom paths
# given in html_static_path.
html_css_files = [
    "mpl.css",
]

html_theme = "pydata_sphinx_theme"

html_theme_options = {
    "github_url": "https://github.com/yuzie007/mpltern",
    "logo": {
       "image_light": "_static/logo_light.svg",
       "image_dark": "_static/logo_dark.svg",
    },
    "header_links_before_dropdown": 10,
}

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

# numpydoc config

numpydoc_show_class_members = False

# Workaround to remove matplotlib warning based on
# https://github.com/sphinx-gallery/sphinx-gallery/pull/521



# Remove matplotlib agg warnings from generated doc when using plt.show
warnings.filterwarnings("ignore", category=UserWarning,
                        message='Matplotlib is currently using agg, which is a'
                                ' non-GUI backend, so cannot show the figure.')
