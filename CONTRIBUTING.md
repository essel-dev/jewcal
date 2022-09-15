# Development
## Install
### Upgrade pip and setuptools
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
```

## Develop
### Test
```sh
tox -e test
```

### Lint
To run all lint checkers:
```sh
tox
```

To run a specific lint checker:
```sh
tox -e flake8
```

### Pre-commit
```sh
pre-commit run --all-files
```

## Document
```sh
sphinx-autobuild --watch . --open-browser docs docs/_build/html
```
