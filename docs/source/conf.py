"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# https://setuptools-scm.readthedocs.io/en/latest/usage/#usage-from-sphinx
from importlib.metadata import version as get_version

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project: str = 'JewCal'
project_copyright: str = 'essel.dev'
author: str = 'essel.dev'
release: str = get_version(project)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: list[str] = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autosectionlabel',
]

templates_path: list[str] = ['_templates']
exclude_patterns: list[str] = []

autodoc_class_signature: str = 'separated'
autodoc_default_options: dict[str, str | bool | None] = {
    'members': True,
    'member-order': 'alphabetical',
    'special-members': '__init__, __str__, __repr__',
    'undoc-members': False,
    'exclude-members': '__weakref__',
}

add_module_names: bool = False
nitpicky = True  # pylint: disable=invalid-name
nitpick_ignore = [
    # https://stackoverflow.com/a/30624034 Bug in the Python docs: references to some
    # of the Python built-ins do not resolve correctly
    ('py:class', 'dataclasses.InitVar'),
    ('py:class', 'datetime.date'),
    ('py:class', 'date'),
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme: str = 'sphinx_rtd_theme'
html_static_path: list[str] = ['_static']

# https://github.com/readthedocs/sphinx_rtd_theme/issues/1301#issuecomment-1219961515
# https://gist.github.com/nocarryr/846301fd5c9083e2243346d19e55b5a3#file-conf-pyL31
# Uncomment this line to set `display: block;` on `.py.property` tags
html_css_files = ['override.css']
