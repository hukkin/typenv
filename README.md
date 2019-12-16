[![Build Status](https://travis-ci.com/hukkinj1/typenv.svg?branch=master)](https://travis-ci.com/hukkinj1/typenv)
[![codecov.io](https://codecov.io/gh/hukkinj1/typenv/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkinj1/typenv)
[![PyPI version](https://badge.fury.io/py/typenv.svg)](https://badge.fury.io/py/typenv)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# typenv

<!--- Don't edit the version line below manually. Let bump2version do it for you. -->
> Version 0.0.3

> Typed environment variable parsing for Python

## Background
Typenv does environment variable parsing with an API almost identical to the excellent [environs](https://github.com/sloria/environs). There are a few reasons why typenv might be preferred:
- Type annotated typecast functions. Type checkers are able to understand types of parsed environment variables.
- More flexible prefix manipulation of environment variable names.
- Validation of environment variable names.
- Optional automatic uppercasing of environment variable names.
- Ability to generate a .env.example that shows expected types of environment variables.
- Less dependencies. No [marshmallow](https://github.com/marshmallow-code/marshmallow) required.

## Installing
Installing from PyPI repository (https://pypi.org/project/typenv):
```bash
pip install typenv
```

## Usage
See [environs README.md](https://github.com/sloria/environs/blob/master/README.md) for now, as the API of typenv is mostly just a subset of environs'.

TODO: Add a more accurate API documentation / usage guide here.

## Acknowledgments
The public API of this library is almost an exact copy of [environs](https://github.com/sloria/environs), which is based on [envparse](https://github.com/rconradharris/envparse) and [django-environ](https://github.com/joke2k/django-environ). Credit for the interface goes to the authors of those libraries.

## Contributing
1. Fork/clone the repository.

1. Install dependencies (you'll probably want to create a virtual environment, using your preferred method, first).
    ```bash
    pip install -r requirements.txt
    ```

1. Install pre-commit hooks
    ```bash
    pre-commit install
    ```

1. After making changes and having written tests, make sure tests pass:
    ```bash
    pytest
    ```

1. Commit, push, and make a PR.
