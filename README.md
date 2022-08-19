# Jewcal
[![Run tests](https://github.com/essel-dev/jewcal/actions/workflows/python-app.yml/badge.svg)](https://github.com/essel-dev/jewcal/actions/workflows/python-app.yml)

Convert Gregorian dates to Jewish dates and get Shabbos / holiday details for Diaspora.

## Local Development
### Code Style
* [PEP 8](https://pep8.org/) linters:
    * flake8
    * pylint
* docstring linters:
    * pydocstyle
    using the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
    * [darglint](https://github.com/terrencepreilly/darglint)
* static type checker:
    * mypy

To run all lint checkers:
```sh
tox
```

To run a specific lint checker:
```sh
tox -e flake8
```

### Install
#### Python
Verify if Python is installed.
```sh
python --version
```

#### Project code
```sh
cd
git clone # path-to-this-repository.git
```

#### Initialize and activate a virtual environment
```sh
cd # path-to-downloaded-reposity
python -m venv env
source env/bin/activate
```

#### Install the dev dependencies
```sh
pip install -e .[dev]
```

### Tests
```sh
tox -e test
```
