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
cd # path-to-downloaded-repository
python -m venv env
source env/bin/activate
```

### Dependencies
```sh
pip install -e .[dev]
```

## Develop
### Test
```sh
tox -e test
```

### Lint
See [tox.ini](tox.ini) for all linters.

To run a specific linter:
```sh
tox -e flake8
```

## Document
```sh
cd docs
make clean
make html
```

The HTML pages are in build/html.
