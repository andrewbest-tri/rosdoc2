# Copyright 2020 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

conf_py_template = """\
# This file was autogenerated by rosdoc2.

# Sphinx extensions.
extensions = [
    'breathe',
    'exhale',
    'sphinx.ext.autodoc',
    # 'sphinx.ext.doctest',
    # 'sphinx.ext.imgmath',
    'sphinx.ext.intersphinx',
]

breathe_projects = {{
    "{package.name} Doxygen Project": "generated/doxygen/xml",
}}
breathe_default_project = "{package.name} Doxygen Project"

# Setup the exhale extension.
exhale_args = {{
    # These arguments are required.
    "containmentFolder": "./api",
    "rootFileName": "library_root.rst",
    "rootFileTitle": "Library API",
    "doxygenStripFromPath": "..",
    # Suggested optional arguments.
    "createTreeView": True,
    # TIP: if using the sphinx-bootstrap-theme, you need
    # "treeViewIsBootstrap": True,
    "exhaleExecutesDoxygen": False,
    "exhaleUseDoxyfile": True,
#    "exhaleDoxygenStdin": \"""\\
#INPUT = {doxygen_input_files}
#GENERATE_HTML = YES{doxygen_tag_file_entries}
#GENERATE_TAGFILE = "generated/doxygen/{package.name}.tag"
#FILE_PATTERNS = *.hpp *.h *.cpp *.c *.cc
#\""",
}}

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'{package.name}'
# TODO(tfoote) The docs say year and author but we have this and it seems more relevant.
copyright = u'{package_licenses}'

version = '{package_version_short}'
release = '{package.version}'

# Output file base name for HTML help builder.
htmlhelp_basename = '{package.name}'

# Intersphinx mapping.
intersphinx_mapping = {{
    'http://docs.python.org/': None,{sphinx_intersphinx_mappings}
}}

autoclass_content = "both"
"""

index_rst_template = """\
{package.name}
{package_underline}

TODO: Package header info


Doxygen Content
===============

:doc:`api/library_root`

:doc:`source/{package.name}`


Sphinx Subprojects
==================

:doc:`source/index`


Indices and Search
==================

* :ref:`genindex`
* :ref:`search`

"""


def setup_doc_build_prefix(
    package_source_directory,
    package_doc_build_directory,
    package,
    tag_files,
    inventory_files,
):
    """Setup the given directory to build the documentation for the given package."""
    # Create TAGFILES entries.
    tag_file_entries = [
        f'TAGFILES +="{tagfile}=http://docs.ros.org/en/latest/p/{package_name}"'
        for package_name, tagfile in tag_files.items()
    ]

    # Create intersphinx mappings.
    intersphinx_mappings = [
        f"'{package_name}': ('http://docs.ros.org/en/latest/p/{package_name}', ('{inv_file}'))"
        for package_name, inv_file in inventory_files.items()
    ]

    # Create variables for templates.
    template_variables = {
        'package_doc_build_directory': package_doc_build_directory,
        'package': package,
        'package_version_short': '.'.join(package.version.split('.')[0:2]),
        'package_licenses': ', '.join(package.licenses),
        'package_underline': '=' * len(package.name),
        'doxygen_input_files': "",
        'doxygen_tag_file_entries': '\n'.join(tag_file_entries),
        'sphinx_intersphinx_mappings': '\n'.join(intersphinx_mappings),
    }

    # Create the standard conf.py and index.rst from templates.
    conf_py = conf_py_template.format_map(template_variables)
    index_rst = index_rst_template.format_map(template_variables)

    with open(os.path.join(package_doc_build_directory, 'conf.py'), 'w') as f:
        f.write(conf_py)

    with open(os.path.join(package_doc_build_directory, 'index.rst'), 'w') as f:
        f.write(index_rst)

    # Link in the source code for the package.
    package_link_in_doc_build_directory = \
        os.path.join(package_doc_build_directory, package.name)
    if not os.path.exists(package_link_in_doc_build_directory):
        if os.path.islink(package_link_in_doc_build_directory):
            os.remove(package_link_in_doc_build_directory)
        os.symlink(
            os.path.relpath(
                package_source_directory,
                start=os.path.dirname(package_link_in_doc_build_directory)),
            package_link_in_doc_build_directory)
