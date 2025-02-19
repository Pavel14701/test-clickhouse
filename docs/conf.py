import os
import sys
sys.path.insert(0, os.path.abspath('../'))

project = 'Test Clickhouse'
copyright = '2025, Pavel Kutsia'
author = 'Pavel Kutsia'
release = '0.1'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.coverage',
    'sphinx.ext.autosummary'
]

autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
language = 'ru'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
