"""Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'JewCal'
copyright = '2023, essel.dev'
author = 'essel.dev'
release = '0.4'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: list[str] = []

templates_path: list[str] = ['_templates']
exclude_patterns: list[str] = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme: str = 'sphinx_rtd_theme'
html_static_path: list[str] = ['_static']
