Python 🚀 Bootstrap
=======================

Unix: ``curl -o start.py https://github.com/andrejanesic/Python-Pip-Make-Starter/start.py | python -``

Windows: ``(Invoke-WebRequest -Uri https://github.com/andrejanesic/Python-Pip-Make-Starter/start.py -UseBasicParsing).Content | python -``

Follow the setup wizard and you'll have a working Python project in seconds.

What is Python 🚀 Bootstrap?
----------------------------

Creating Python projects by hand can be difficult and complex.

How do you structure your project? Which package manager to use? And what about build scripts?

That's where **Python 🚀 Bootstrap** comes into play.

Python 🚀 Bootstrap helps you set up a new Python project in seconds.

From ``setup.py`` to test module, from ``.gitignore`` to ``Make``, Python 🚀 Bootstrap builds everything for you.

Just follow the setup wizard, and you'll get a fully-working Python 3 project in less than a minute.

How to Use?
-----------

Simply copy ``start.py`` into your project directory and execute with Python:

**Unix:**

``curl -o start.py https://github.com/andrejanesic/Python-Pip-Make-Starter/start.py | python -``

**Windows:**

``(Invoke-WebRequest -Uri https://github.com/andrejanesic/Python-Pip-Make-Starter/start.py -UseBasicParsing).Content | python -``

Follow the provided steps to complete your project setup.

Project Structure
-----------------
::
    package_name/ .......... The main module of your program. Write your code here.
        __init__.py ........ Initializes the module. Export your .py files here.
        __main__.py ........ Module's main script.
        core.py ............ Write your program here. You may also create additional
                             script files and subdirectories here.
    tests/ ................. The test suite of your project.
        __init__.py ........ Initializes the test module.
        __main__.py ........ Runs the tests.
        test_basic.py ...... An example test script. You may also create additional
                             test scripts here.
    .gitignore ............. Basic gitignore, automatically ignores venv dir.
    make.bat ............... The Make scripts for testing, running and building your
    Makefile ............... project. Extend the scripts to your specific needs.
    MANIFEST.in ............ Specifies which files to include in source distribution.
    README.rst ............. Auto-generated README.
    requirements.txt ....... File to place your pip requirements.
    setup.py ............... Auto-generated based on project info.

Authors
-------

.. image:: https://andrejanesic.com/git-signature-sm.png
    :width: 359
    :alt: Andreja Nesic

| **Andreja Nesic** \[`LinkedIn <https://www.linkedin.com/in/andreja-nesic/>`__\]
| Comp Sci Undergrad @ `School of Computing, Belgrade <https://www.linkedin.com/school/racunarski-fakultet/>`__
| office@andrejanesic.com
| anesic3119rn@raf.rs

References
----------

This project is based on the following projects, research, documents, etc:

- `Reitz, K et al. The Hitchhiker's Guide to Python - Structuring Your Project. https://docs.python-guide.org/writing/structure/ (Accessed Jan 2023) <https://docs.python-guide.org/writing/structure/>`__

- `Reitz, K et al. "setup.py (for humans)". https://github.com/kennethreitz/setup.py (Accessed Jan 2023) <https://github.com/kennethreitz/setup.py>`__