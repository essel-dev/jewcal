# Local Development
## Install
### Python
Verify if Python is installed.
```sh
python --version
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

## Test
```sh
tox -e test
```

## Linters
To run all lint checkers:
```sh
tox
```

To run a specific lint checker:
```sh
tox -e flake8
```
