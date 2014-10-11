import sys
import re
import os

import sphinx.ext.autodoc

#on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
sys.path.insert(0, os.path.abspath('../..'))

import amqpy

needs_sphinx = '1.2'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode'
]

# configure autodoc member grouping and ordering
sphinx.ext.autodoc.DataDocumenter.member_order = 5
sphinx.ext.autodoc.AttributeDocumenter.member_order = 6
sphinx.ext.autodoc.InstanceAttributeDocumenter.member_order = 7
autodoc_member_order = 'groupwise'
autodoc_default_flags = ['members', 'show-inheritance']

intersphinx_mapping = {'http://docs.python.org/3.4': None}

templates_path = ['_templates']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'amqpy'
copyright = '2014, V G'

# The short X.Y version.
version = amqpy.__version__
# The full version, including alpha/beta/rc tags.
release = amqpy.__version__

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The reST default role (used for this markup: `text`) to use for all
# documents.
# default_role = None

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
# add_module_names = True

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.

html_theme_path = ['_theme']
html_theme = 'bootstrap'
html_theme_options = {
    # Tab name for entire site. (Default: "Site")
    'navbar_site_name': 'amqpy Docs',

    # Render the next and previous page links in navbar. (Default: true)
    'navbar_sidebarrel': False,

    # Render the current pages TOC in the navbar. (Default: true)
    #'navbar_pagenav': True,

    # Tab name for the current pages TOC. (Default: "Page")
    'navbar_pagenav_name': 'Page',

    # Global TOC depth for "site" navbar tab. (Default: 1)
    # Switching to -1 shows all levels.
    'globaltoc_depth': 2,

    # Include hidden TOCs in Site navbar?
    #
    # Note: If this is "false", you cannot have mixed ``:hidden:`` and
    # non-hidden ``toctree`` directives in the same page, or else the build
    # will break.
    #
    # Values: "true" (default) or "false"
    #'globaltoc_includehidden': "true",

    # HTML navbar class (Default: "navbar") to attach to <div> element.
    # For black navbar, do "navbar navbar-inverse"
    #'navbar_class': "navbar",

    # Fix navigation bar to top of page?
    # Values: "true" (default) or "false"
    'navbar_fixed_top': 'true',

    # Location of link to source.
    # Options are "nav" (default), "footer" or anything else to exclude.
    'source_link_position': 'nav',

    # Bootswatch (http://bootswatch.com/) theme.
    #
    # Options are nothing with "" (default) or the name of a valid theme
    # such as "amelia" or "cosmo".
    'bootswatch_theme': 'flatly',
}

html_static_path = ['_static']

# Custom sidebar templates, maps document names to template names.
# html_sidebars = {}

# Output file base name for HTML help builder.
htmlhelp_basename = 'amqpydoc'


def get_field(doc: str, name: str):
    match = re.search(':{}: (.*)$'.format(name), doc, re.IGNORECASE | re.MULTILINE)
    if match:
        return match.group(1).strip()


def process_sig(app, what, name, obj, options, signature, return_annotation):
    doc = str(obj.__doc__)
    otype = str(type(obj))
    msg_meth = '{what:11} {otype:23} {name:50} -> {rt}'
    msg_class = '{what:11} {otype:23} {name:50} {sig}'

    rt = None
    if what == 'method' and not name.endswith('__init__'):
        if 'rtype' in doc:
            rt = get_field(doc, 'rtype')
            print(msg_meth.format(**locals()))
        else:
            # assume methods with undocumented rtype return `None`
            rt = 'None'
            print(msg_meth.format(**locals()))
    elif type(obj) is property:
        if 'rtype' in doc:
            rt = get_field(doc, 'rtype')
            print(msg_meth.format(**locals()))
        else:
            rt = '?'
            print(msg_meth.format(**locals()))
    elif what == 'class':
        # bases = []
        # for cls in obj.__bases__:
        #     bases.append('{}.{}'.format(cls.__module__, cls.__name__))
        # sig = ', '.join(bases)
        # sig = '({})'.format(sig)
        sig = ''
        print(msg_class.format(**locals()))
        return sig, None
    else:
        rt = 'skip'
        print(msg_meth.format(**locals()))

    if rt and rt not in ['?', 'skip']:
        return signature, rt


def process_doc(app, what, name, obj, options, lines):
    otype = str(type(obj))
    msg = '{what:11} {otype:23} {name:50}'
    if type(obj) == property:
        s = '`(property)`'
        lines.insert(0, s)


def setup(app):
    app.connect('autodoc-process-signature', process_sig)
    app.connect('autodoc-process-docstring', process_doc)
