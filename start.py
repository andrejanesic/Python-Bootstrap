# -*- coding: utf-8 -*-

"""
MIT License

Copyright (c) 2023 Andreja Nesic

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import re
import sys
import os
import argparse

"""
Launch this script to quickly set up the project.
"""

### Script args ###
args = None


### Template files ###

TEMPLATE_SETUP = """# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    %s%s%s%s%s%s%slong_description=readme,
    license=license,
    packages=find_packages(exclude=[
        "tests", "*.tests", "*.tests.*", "tests.*",
        "docs",  "*.docs",  "*.docs.*",  "docs.*"
    ])
)"""

TEMPLATE_MAKEFILE = """init:
    python -m venv env
    ./env/Scripts/activate
	pip install -r requirements.txt

dev:
    ./env/Scripts/activate
    python -m %s

test:
    ./env/Scripts/activate
    python -m tests

build:
    ./env/Scripts/activate
    python setup.py sdist"""

TEMPLATE_MAKE_BAT = """@ECHO OFF

if "%%1" == "" goto init

if "%%1" == "init" (
	:init
    python -m venv env
    call .\\env\\Scripts\\activate.bat
	pip install -r requirements.txt
	goto end
)

if "%%1" == "dev" (
	:init
    call .\\env\\Scripts\\activate.bat
	python -m %s
	goto end
)

if "%%1" == "test" (
	:init
    call .\\env\\Scripts\\activate.bat
	python -m tests
	goto end
)

if "%%1" == "build" (
	:init
    call .\\env\\Scripts\\activate.bat
	python setup.py sdist
	goto end
)

:end"""

TEMPLATE_README = """%s
%s

%s

Setup & Commands
----------------

Please run ``./make`` (Linux) or ``.\make.bat`` (Windows) to set up the package. This will create a new Python `virtual environment <https://docs.python.org/3/library/venv.html>`__ and install the required dependencies.

The following Make commands are available. Use ``make (command)`` syntax on Linux and ``.\make.bat (command)`` syntax on Windows:

- ``init``: Initializes the package by installing the required repositories.

- ``dev``: Runs the program's main package.

- ``test``: Runs the test suite.

- ``build``: Builds the package.
"""

TEMPLATE_README_AUTHORS = """\n\nAuthors
-------

%s
%s
"""

TEMPLATE_INIT = """# -*- coding: utf-8 -*-

from .core import *
"""

TEMPLATE_CORE = """# -*- coding: utf-8 -*-

def main():
    # Your code here...
    print("Hello World")
    return "Hello World"
"""

TEMPLATE_MAIN = """# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from .core import main
    main()
"""

TEMPLATE_TEST_INIT = """# -*- coding: utf-8 -*-

from .test_basic import *
"""

TEMPLATE_TEST_BASIC = """# -*- coding: utf-8 -*-

import unittest
from %s import *

class BasicTestSuite(unittest.TestCase):
    \"""
    Test cases here...
    \"""

    def test_main(self):
        self.assertEquals(main(), "Hello World")
"""

TEMPLATE_TEST_MAIN = """# -*- coding: utf-8 -*-

if __name__ == "__main__":
    from .test_basic import *
    import unittest
    unittest.main()
"""

TEMPLATE_GITIGNORE = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*,cover
.hypothesis/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# IPython Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# dotenv
.env

# virtualenv
.venv/
venv/
ENV/

# Spyder project settings
.spyderproject

# Rope project settings
.ropeproject

# IDEs
.idea/
.vscode/"""

### Functions ###


def log(msg: str) -> None:
    """
    Logs to console.
    """

    global args

    if args and not args.quiet:
        print(msg)


def error(err: str) -> None:
    """
    Prints error and exits.
    """
    log(f"[ERROR] {err}")
    log(f"[ERROR] Project setup failed.")
    sys.exit(0)


def warning(msg: str) -> None:
    """
    Prints a warning message.
    """
    log(f"[WARNING] {msg}")


def info(msg: str) -> None:
    """
    Prints an info message.
    """
    log(f"[INFO] {msg}")


def query(
    text: str,
    pat: str = None,
    dflt: str = None
) -> str:
    """
    Queries the user to get the input
    string. Validates the input string
    against given regex pattern. If
    string empty or None, returns
    default version. If regex not
    matched, throws error.
    """
    global args

    if args and args.quiet:
        text = ""
    inp = input(text).strip()

    if not inp and dflt:
        inp = dflt

    if pat:
        if not re.match(pat, inp):
            error(f"String must match pattern: {pat}")

    inp = inp.replace("\\", "\\\\")
    inp = inp.replace("'", "\\'")
    inp = inp.replace("\"", "\\\"")
    return inp


def write_file(fname: str, content: str):
    """
    Creates the file on fname path
    and writes the given content.
    """

    force_write = True

    if os.path.exists(fname):
        force_write = input(
            f"File {fname} already exists. Overwrite? (Y/n) ")

        force_write = force_write.strip().lower()

        if not force_write:
            force_write = True
            info("Overwriting...")
        else:
            force_write = (force_write == "y")

    if force_write:
        with open(fname, "w") as f:
            f.write(content)


def build_readme(
        name: str,
        description: str,
        author: str = None,
        author_email: str = None):
    """
    Creates the README file contents
    and writes it.
    """

    content = TEMPLATE_README % (name, "=" * len(name), description)

    if author and author_email:
        content += TEMPLATE_README_AUTHORS % (author, author_email)

    write_file("./README.rst", content)


def build_manifest(files: list = ["LICENSE", "README.rst"]):
    """
    Creates the MANIFEST file contents
    and writes it.
    """

    content = ""
    for f in files:
        content += f"{f}\n"
    content = content.strip()
    write_file("./MANIFEST.in", content)


def build_makefiles(package: str):
    """
    Creates the Make and make.bat file
    contents and writes them.
    """

    write_file("./Makefile", (TEMPLATE_MAKEFILE % package))
    write_file("./make.bat", (TEMPLATE_MAKE_BAT % package))


def build_setup(
    package: str,
    version: str = None,
    description: str = None,
    python_requires: str = None,
    author: str = None,
    author_email: str = None,
    url: str = None
):
    """
    Creates the setup.py file contents
    and writes it.
    """

    def formatted(inp: str, keyword: str, dflt: str = ""):
        if not inp:
            return dflt
        else:
            return f"{keyword}='{inp}',\n\t"

    package = re.sub(r"^[^a-zA-Z]*", "", package.strip().lower())
    package = re.sub(r"[^a-zA-Z_]*", "", package)
    package = formatted(package, "name")
    version = formatted(version, "version")
    description = formatted(description, "description")
    author = formatted(author, "author")
    author_email = formatted(author_email, "author_email")
    url = formatted(url, "url")
    python_requires = formatted(python_requires, ">=3.7.0")

    content = TEMPLATE_SETUP % (package, version, description, author, author_email, url, python_requires)

    write_file("./setup.py", content)


def build_gitignore():
    """
    Writes the .gitignore file.
    """
    write_file(".gitignore", TEMPLATE_GITIGNORE)


def build_module(package: str):
    """
    Builds the main package dir
    and tests dir.
    """

    if os.path.exists(f"./{package}"):
        error(
            f"Package directory {package} already occupied or file exists. Please delete file/dir to continue.")

    if os.path.exists(f"./tests"):
        error(
            f"Tests directory tests already occupied or file exists. Please delete file/dir to continue.")

    os.mkdir(f"./{package}")
    write_file(f"./{package}/__init__.py", TEMPLATE_INIT)
    write_file(f"./{package}/__main__.py", TEMPLATE_MAIN)
    write_file(f"./{package}/core.py", TEMPLATE_CORE)

    os.mkdir(f"./tests")
    write_file(f"./tests/__init__.py", TEMPLATE_TEST_INIT)
    write_file(f"./tests/__main__.py", TEMPLATE_TEST_MAIN)
    write_file(f"./tests/test_basic.py", TEMPLATE_TEST_BASIC % package)


def build_requirements():
    """
    Creates the requirements.txt file.
    """

    write_file("./requirements.txt", "")


def build_all(
    name: str,
    package: str,
    version: str = None,
    description: str = None,
    python_requires: str = None,
    author: str = None,
    author_email: str = None,
    url: str = None
):
    """
    Creates all the required project files.
    """

    build_makefiles(package)
    build_manifest()
    build_readme(
        name,
        description,
        author,
        author_email
    )
    build_setup(
        package,
        version,
        description,
        python_requires,
        author,
        author_email,
        url
    )
    build_requirements()
    build_gitignore()
    build_module(package)
    cleanup()


def cleanup():
    """
    Removes quickstart files.
    """

    if os.path.exists("./start.py"):
        os.unlink("./start.py")


def parse_args() -> None:
    """
    Sets up and parses program args.
    """

    global args

    parser = argparse.ArgumentParser(
        prog="Python-Pip-Make-Starter",
        description="Quickly set up your Python project",
    )

    parser.add_argument("-n", "--name",
                        type=str,
                        dest="name",
                        help="Project name",
                        required=False,
                        default=None)

    parser.add_argument("-p", "--package",
                        type=str,
                        dest="package",
                        help="Package name (PEP8-compliant)",
                        required=False,
                        default=None)

    parser.add_argument("-v", "--version",
                        type=str,
                        dest="version",
                        help="Version number",
                        required=False,
                        default=None)

    parser.add_argument("-d", "--description",
                        type=str,
                        dest="description",
                        help="Project description",
                        required=False,
                        default=None)

    parser.add_argument("-a", "--author",
                        type=str,
                        dest="author",
                        help="Author name",
                        required=False,
                        default=None)

    parser.add_argument("-e", "--email",
                        type=str,
                        dest="author_email",
                        help="Author email",
                        required=False,
                        default=None)

    parser.add_argument("-u", "--url",
                        type=str,
                        dest="url",
                        help="Project URL",
                        required=False,
                        default=None)

    parser.add_argument("-pr", "--python",
                        type=str,
                        dest="python_requires",
                        help="Required Python version (PEP423-compliant)",
                        required=False,
                        default=None)

    parser.add_argument("-q", "--quiet",
                        action='store_true',
                        dest="quiet",
                        help="Logs nothing",
                        required=False,
                        default=False)

    args = parser.parse_args()


def main() -> None:
    global args
    parse_args()

    log("--- Enter project info ---")

    name = args.name
    if not name:
        name = query("Project name (Python Project): ",
                     r"^.+$", "Python Project")

    package = args.package
    if not package:
        package_default = re.sub(r"[^a-zA-Z_]", "", name.lower())
        package_default = re.sub(r"^[_]*", "", package_default)
        package = query("Package name (%s): " %
                        package_default, r"^[a-zA-Z]+[a-zA-Z_]+$", package_default)

    version = args.version
    if not version:
        version = query("Version number (1.0.0): ", r"^.+$", "1.0.0")

    description = args.description
    if not description:
        description = query("Description (Sample Python project): ",
                            r".+$", "Sample Python project")

    author = args.author
    if not author:
        author = query("Author (empty): ", r"^.*$", "")

    author_email = args.author_email
    if not author_email:
        author_email = query("Author email (empty): ", r"^.*$", "")

    url = args.url
    if not url:
        url = query("Project URL (empty): ", r"^.*$", "")

    python_requires = args.python_requires
    if not python_requires:
        python_requires = query(
            "Requires Python (>=3.7.0): ", r"^.+$", ">=3.7.0")

    build_all(
        name,
        package,
        version,
        description,
        author,
        author_email,
        url,
        python_requires
    )

    if not os.path.exists("./LICENSE"):
        warning("Don't forget to add a license into LICENSE file!")

    info("Setup complete.")


if __name__ == "__main__":
    main()
