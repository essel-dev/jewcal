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

### Project code
```sh
cd && git clone # path-to-this-repository.git
```

### Virtual environment
```sh
cd # path-to-downloaded-reposity
python -m venv .env
source .env/bin/activate
```

### pip and setuptools
```sh
python -m pip install --upgrade pip setuptools
```

### Dependencies
```sh
pip install -e .[dev]
```

### Pre-commit
```sh
pre-commit install
pre-commit autoupdate
pre-commit run --all-files
```

## Develop
### Tox
See [tox](pyproject.toml) for all test environments.

To run all:
```sh
tox
```

To run a specific environment:
```sh
tox -e py311
```

To generate documentation:
```sh
cd docs
make clean html
```
The HTML pages are in build/html.
