# Local Development
## Install
### Python
Verify if Python is installed.
```sh
python --version
```

To install multiple Python versions, use [pyenv](https://github.com/pyenv/pyenv).
To activate:
```sh
pyenv local 3.10 3.11
```

### pip and setuptools
```sh
python -m pip install --upgrade pip setuptools
```

### Project code
```sh
cd
git clone # path-to-this-repository.git
```

### Virtual environment
```sh
cd # path-to-downloaded-reposity
python -m venv env
source env/bin/activate
```

### Dependencies
```sh
pip install -e .[dev]
```

### Pre-commit
```sh
pre-commit install
pre-commit run --all-files
pre-commit autoupdate
```

https://pre-commit.com/

## Develop
### Lint
See [tox](pyproject.toml) for all linters.

To run a specific linter:
```sh
tox -e flake8
```

### Test
```sh
tox -e py311
```

### Document
```sh
make clean html -C docs/
```
The HTML pages are in docs/build/html.
