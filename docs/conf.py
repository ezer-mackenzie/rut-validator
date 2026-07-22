# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------
project = "rut-validator"
copyright = "2024, Eli-ezer Reuven Ramirez Ruiz"
author = "Eli-ezer Reuven Ramirez Ruiz"
release = "0.1.0"

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "README_EMAILSTR.md"]

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"

# -- Extension configuration --------------------------------------------------
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# -- MyST configuration ------------------------------------------------------
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "html_admonition",
    "html_image",
    "replacements",
    "smartquotes",
    "strikethrough",
    "substitution",
    "tasklist",
]

myst_heading_anchors = 3
