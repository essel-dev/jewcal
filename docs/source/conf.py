"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# https://setuptools-scm.readthedocs.io/en/latest/usage/#usage-from-sphinx
from importlib.metadata import version as get_version
from typing import Optional, Union

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
]

templates_path: list[str] = ['_templates']
exclude_patterns: list[str] = []

autodoc_class_signature: str = 'separated'
autodoc_default_options: dict[str, Optional[Union[str, bool]]] = {
    'members': None,
    'member-order': 'alphabetical',
    'special-members': '__init__, __str__, __repr__',
    'undoc-members': False,
    'exclude-members': '__weakref__'
}

add_module_names: bool = False

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme: str = 'sphinx_rtd_theme'
html_static_path: list[str] = ['_static']
