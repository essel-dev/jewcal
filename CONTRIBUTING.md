# Local Development
## Install
### Project code
```sh
cd && git clone # path-to-this-repository.git
```

### uv
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

https://docs.astral.sh/uv/getting-started/installation/

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
uvx tox
```

To run a specific environment:
```sh
uvx tox -e py311
```

To generate documentation:
```sh
uvx tox -e docs
```
The HTML pages are in docs/build/html.
