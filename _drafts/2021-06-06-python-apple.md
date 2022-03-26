---
date: "2021-06-06"
title: "Python Apple"
---
<!-- markdownlint-disable MD025 -->
# Python Apple
<!-- markdownlint-enable MD025 -->

## Python

[pyenv](https://github.com/pyenv/pyenv#basic-github-checkout)

Use `pyenv` to setup python seperately from the system's python and create virtual python instances that automatically start when you `cd` to specific directories.

### Virtual environments

Use conda (Mamba) seperately from venv. Conda is a generalised package manager, venv is for python only.

[A Guide to Python’s Virtual Environments](https://towardsdatascience.com/virtual-environments-104c62d48c54)
[The definitive guide to Python virtual environments with conda](https://en.whiteboxml.com/blog/the-definitive-guide-to-python-virtual-environments-with-conda)
[The Definitive Guide to Conda Environments](https://towardsdatascience.com/a-guide-to-conda-environments-bc6180fc533)

### Conda (Mamba)

Try to install all the dependencies (perhaps using a `requirements.txt` generated from a environment like this `pip freeze > requirements.txt`) at the same time. e.g. `conda create -n octopus requests numpy pandas`

[Mamba](https://mamba.readthedocs.io/en/latest/user_guide/mamba.html)
[Conda or Mamba for production?](https://labs.epi2me.io/conda-or-mamba-for-production/)
use Mambaforge download the latest from https://github.com/conda-forge/miniforge `bash Mambaforge-MacOSX-arm64.sh -b` This is based on conda. Use `conda activate base` then create a `conda env create [envrionment]` and activate it.

### Python venv

[venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)

`python -m venv venv` inside each python project for a full isolated environment

### Testing

don't forget that files need to be called `test_*.py` or `*_test.py`

* [pytest](https://docs.pytest.org/)
* [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
* [Property based testing]https://hypothesis.readthedocs.io/en/latest/

* [Manage Jupyter Notebook and JupyterLab with Systemd - Parametric Thoughts](https://janakiev.com/blog/jupyter-systemd/)

* [Python Programming And Numerical Methods: A Guide For Engineers And Scientists — Python Numerical Methods](https://pythonnumericalmethods.berkeley.edu/notebooks/Index.html)
* [Try/Except — Python Numerical Methods](https://pythonnumericalmethods.berkeley.edu/notebooks/chapter10.03-Try-Except.html)
* [Study Guide: Intro to Computing with Finite Difference Methods](http://hplgit.github.io/INF5620/doc/pub/lecture_decay-1.html#5620:about)
* [StrictYAML - HitchDev](https://hitchdev.com/strictyaml/)
* [Build a YAML document from scratch in code - HitchDev](https://hitchdev.com/strictyaml/using/alpha/howto/build-yaml-document/)

## Visitors

### Python Cookbook

All of this predates Python 3.4 when singledispatch-functools first appeared

8.21. Implementing the Visitor Pattern
8.22. Implementing the Visitor Pattern Without Recursion
9.24. Parsing and Analyzing Python Source

* [Arpeggio/__init__.py at master · textX/Arpeggio · GitHub](https://github.com/textX/Arpeggio/blob/master/arpeggio/__init__.py)
* [Semantic analysis - Arpeggio](http://textx.github.io/Arpeggio/stable/semantics/)

* [WHY YOU DON’T NEED DESIGN PATTERNS IN PYTHON?](https://ep2017.europython.eu/media/conference/slides/why-you-dont-need-design-patterns-in-python.pdf)
* [Function overloading with singledispatch-functools - GeeksforGeeks](https://www.geeksforgeeks.org/function-overloading-with-singledispatch-functools/)
* [functools — Higher-order functions and operations on callable objects — Python 3.9.5 documentation](https://docs.python.org/3/library/functools.html)
* [Built-in Functions — Python 3.9.5 documentation](https://docs.python.org/3/library/functions.html#staticmethod)
* [Glossary — Python 3.9.5 documentation](https://docs.python.org/3/glossary.html)
* [PEP 614 — Relaxing Grammar Restrictions On Decorators | Python.org](https://www.python.org/dev/peps/pep-0614/)
* [PEP 3119 — Introducing Abstract Base Classes | Python.org](https://www.python.org/dev/peps/pep-3119/)
* [3. Data model — Python 3.9.5 documentation](https://docs.python.org/3/reference/datamodel.html#emulating-callable-objects)
* [How can I use functools.singledispatch with instance methods? | Newbedev](https://newbedev.com/how-can-i-use-functools-singledispatch-with-instance-methods)
* [Generic Functions with Python’s Singledispatch | Red’s Digressions](https://rednafi.github.io/digressions/python/2020/04/05/python-singledispatch.html)
* [2.1. What is Data? — Python: From None to Machine Learning](https://python.astrotech.io/machine-learning/introduction/data.html)
* [PEP 443 — Single-dispatch generic functions | Python.org](https://www.python.org/dev/peps/pep-0443/)
* [PEP 318 — Decorators for Functions and Methods | Python.org](https://www.python.org/dev/peps/pep-0318/)
* [Python Advanced: Easy Introduction into Decorators and Decoration](https://www.python-course.eu/python3_decorators.php)
* [Primer on Python Decorators – Real Python](https://realpython.com/primer-on-python-decorators/)
* [Python Class Method Decorator @classmethod](https://www.tutorialsteacher.com/python/classmethod-decorator)

* [mypy - Optional Static Typing for Python](http://mypy-lang.org)
* [PyPy: Faster Python With Minimal Effort – Real Python](https://realpython.com/pypy-faster-python/)
* [PyPy](https://www.pypy.org)

## Links

### iPad

* [Using an iPad for Data Science in 2021!](https://towardsdatascience.com/using-an-ipad-for-data-science-in-2021-d6a973dd27ab)
* [My top Python IDEs for iPad](https://blog.devgenius.io/my-top-python-ides-for-ipad-3f777023155c)
* [Jupyter for iOS | Juno](https://juno.sh)
* [Carnets - Jupyter](https://holzschu.github.io/Carnets_Jupyter/)
* [Pythonista-Tools/Utilities.md at master · Pythonista-Tools/Pythonista-Tools · GitHub](https://presstige.io/p/Pythonista-Tools-Utilities-md-at-master-Pythonista-Tools-Pythonista-Tools-GitHub-081da1843127457d994ab76f11733f4c)
* [GitHub - Pythonista-Tools/Pythonista-Tools: Gathering code and links to projects specially developed for Pythonista for iOS.](https://github.com/Pythonista-Tools/Pythonista-Tools)
* [Thoughts on iOS Python - All this](https://leancrew.com/all-this/2020/03/thoughts-on-ios-python/)
* [GitHub - idcrook/awesome-pythonista: Collection of Pythonista 3 (iOS app) scripts and things](https://github.com/idcrook/awesome-pythonista)

### General

* [Stupid Python Ideas: How do I make a recursive function iterative?](http://stupidpythonideas.blogspot.com/2014/10/how-do-i-make-recursive-function.html)

### Mac setup

* [Virtual Environments and Packages](https://docs.python.org/3/tutorial/venv.html)
* [Simple Python Version Management: pyenv](https://github.com/pyenv/pyenv)
* [pyenv-virtualenv is a pyenv plugin that provides features to manage virtualenvs and conda environments for Python on UNIX-like systems.](https://github.com/pyenv/pyenv-virtualenv)
* [Python Development on macOS with pyenv](https://jordanthomasg.medium.com/python-development-on-macos-with-pyenv-2509c694a808)
* [Python Development on macOS with pyenv-virtualenv](https://jordanthomasg.medium.com/python-development-on-macos-with-pyenv-virtualenv-ec583b92934c)

* [The right and wrong way to set Python 3 as default on a Mac](https://opensource.com/article/19/5/python-3-default-mac)

* [How to manage multiple Python versions and virtual environments](https://www.freecodecamp.org/news/manage-multiple-python-versions-and-virtual-environments-venv-pyenv-pyvenv-a29fb00c296f/)
* [Python settings reference](https://code.visualstudio.com/docs/python/settings-reference#_general-settings)
* [User and Workspace Settings](https://code.visualstudio.com/docs/getstarted/settings)
* [Using Python Virtual Environment in VSCode](https://techinscribed.com/python-virtual-environment-in-vscode/)

<!-- markdownlint-disable MD034 -->

<!-- markdownlint-enable MD034 -->
