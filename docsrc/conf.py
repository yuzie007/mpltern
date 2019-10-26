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

import mpltern


# General configuration
# ---------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'numpydoc',  # Needs to be loaded *after* autodoc.
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


intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://docs.scipy.org/doc/numpy/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/reference/', None),
}


# Sphinx gallery configuration
sphinx_gallery_conf = {
    'examples_dirs': ['../examples'],
    'filename_pattern': '^((?!sgskip).)*$',
    'gallery_dirs': ['gallery'],
    'doc_module': ('mpltern', ),
    'reference_url': {
        'mpltern': None,
        'numpy': 'https://docs.scipy.org/doc/numpy',
        'scipy': 'https://docs.scipy.org/doc/scipy/reference',
    },
    'min_reported_time': 1,
    # The following is commented out because SVG does not work nicely yet
    # for `ax.pcolormesh(shading='gouraud')
    'image_scrapers': (matplotlib_svg_scraper(),),
}

plot_gallery = 'True'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'

# This is the default encoding, but it doesn't hurt to be explicit
source_encoding = "utf-8"

project = 'Mpltern'
copyright = '2019, Yuji Ikeda'
author = 'Yuji Ikeda'

version = mpltern.__version__
# The full version, including alpha/beta/rc tags.
release = version

# Plot directive configuration
# ----------------------------

plot_formats = [('png', 100), ('pdf', 100)]

# GitHub extension

github_project_url = "https://github.com/yuzie007/mpltern/"

# Options for HTML output
# -----------------------
html_theme = 'basic'
html_style = 'mpltern.css'

# The name of an image file (within the static path) to place at the top of
# the sidebar.
html_logo = '_static/sphx_glr_logos0_003.svg'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If nonempty, this is the file name suffix for generated HTML files.  The
# default is ``".html"``.
html_file_suffix = '.html'

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%b %d, %Y'

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# # Custom sidebar templates, maps page names to templates.
# html_sidebars = {
#     '**': ['searchbox.html', 'localtoc.html', 'relations.html',
#            'pagesource.html']
# }

# If false, no module index is generated.
# html_use_modindex = True
html_domain_indices = ["py-modindex"]

# Path to favicon
html_favicon = '_static/favicon.png'

# Workaround to remove matplotlib warning based on
# https://github.com/sphinx-gallery/sphinx-gallery/pull/521


import warnings

# Remove matplotlib agg warnings from generated doc when using plt.show
warnings.filterwarnings("ignore", category=UserWarning,
                        message='Matplotlib is currently using agg, which is a'
                                ' non-GUI backend, so cannot show the figure.')
