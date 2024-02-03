# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Guajira-Coin'
copyright = '2024, Dilan Gonzalez, Luz Moronta'
author = 'Dilan Gonzalez, Luz Moronta'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

language = 'es'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_favicon = '_static/favicon.ico'  # Ruta al archivo de ícono
html_context = {
    'meta_description': 'Minería de Criptomonedas con ESP8266',
    'meta_keywords': 'ESP8266, Guajira, Criptomonedas, GuajiraCoin, Guajira-Coin, Dilan Gonzalez, Luz Moronta',
    'og_image': '_static/guajiracoin.jpg',
    'og_description': 'Minando la criptomoneda Guajira-Coin utilizando un microcontrolador',
}
