"""Configuration file for the Sphinx documentation builder."""

#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'JewCal'
copyright = 'essel.dev'
author = 'essel.dev'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.duration',
]

templates_path = ['_templates']

autodoc_class_signature = 'separated'
autodoc_default_options = {
    'members': None,
    'member-order': 'alphabetical',
    'special-members': '__init__, __str__, __repr__',
    'undoc-members': False,
    'exclude-members': '__weakref__'
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

html_theme_options = {
    'description': (
        'Jewish Calendar for Diaspora and Israel with holidays and fasts.'
    ),
    'fixed_sidebar': True,
}

html_show_sourcelink = False
