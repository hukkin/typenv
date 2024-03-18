[![Build Status](https://github.com/hukkin/typenv/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkin/typenv/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)
[![codecov.io](https://codecov.io/gh/hukkin/typenv/branch/master/graph/badge.svg)](https://codecov.io/gh/hukkin/typenv)
[![PyPI version](https://img.shields.io/pypi/v/typenv)](https://pypi.org/project/typenv)

# typenv

<!--- Don't edit the version line below manually. Let bump2version do it for you. -->

> Version 0.2.0

> Typed environment variable parsing for Python

**Table of Contents**  *generated with [mdformat-toc](https://github.com/hukkin/mdformat-toc)*

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Background](#background)
- [Installing](#installing)
- [Usage](#usage)
  - [Basics](#basics)
  - [Supported types](#supported-types)
  - [Default values](#default-values)
  - [Name prefixes](#name-prefixes)
  - [Name character set](#name-character-set)
  - [Name uppercasing](#name-uppercasing)
  - [Validation](#validation)
  - [Reading from a `.env` file](#reading-from-a-env-file)
  - [Dumping parsed values](#dumping-parsed-values)
- [Acknowledgments](#acknowledgments)

<!-- mdformat-toc end -->

## Background<a name="background"></a>

Typenv does environment variable parsing with an API almost identical to the excellent [environs](https://github.com/sloria/environs).
There are a few reasons why typenv might be preferred:

- Type annotated typecast functions: type checkers are able to understand types of parsed environment variables.
- More flexible prefix manipulation of environment variable names.
- Validation of environment variable names.
- Optional automatic uppercasing of environment variable names.
- Ability to generate a .env.example that shows expected types of environment variables.
- Less dependencies. No [marshmallow](https://github.com/marshmallow-code/marshmallow) required.

## Installing<a name="installing"></a>

Installing from PyPI repository (https://pypi.org/project/typenv):

```bash
pip install typenv
```

## Usage<a name="usage"></a>

### Basics<a name="basics"></a>

Set environment variables:

```bash
export NAME='Harry Potter'
export AGE=14
export IS_WIZARD=true
export PATRONUM_SUCCESS_RATE=0.92
export BANK_BALANCE=134599.01
export LUCKY_NUMBERS=7,3,11
export EXTRA_DETAILS='{"friends": ["Hermione", "Ron"]}'
export FAVORITE_COLOR=0x7f0909
```

Parse the values in Python:

```python
from typenv import Env

env = Env()

NAME = env.str("NAME")  # => "Harry Potter"
AGE = env.int("AGE")  # => 14
IS_WIZARD = env.bool("IS_WIZARD")  # => True
PATRONUM_SUCCESS_RATE = env.float("PATRONUM_SUCCESS_RATE")  # => 0.92
BANK_BALANCE = env.decimal("BANK_BALANCE")  # => decimal.Decimal("134599.01")
LUCKY_NUMBERS = env.list("LUCKY_NUMBERS", subcast=int)  # => [7, 3, 11]
EXTRA_DETAILS = env.json("EXTRA_DETAILS")  # => {"friends": ["Hermione", "Ron"]}
FAVORITE_COLOR = env.bytes("FAVORITE_COLOR", encoding="hex")  # => b"\x7f\t\t"

# Optional settings must have a default value
IS_DEATH_EATER = env.bool("IS_DEATH_EATER", default=False)  # => False
```

### Supported types<a name="supported-types"></a>

The types supported by typenv are:

- `env.str`
- `env.int`
- `env.bool`
- `env.float`
- `env.decimal`
- `env.list`
  - Takes a `subcast` keyword argument for casting list items to one of `str`, `int` , `bool`, `float` or `decimal.Decimal`
- `env.json`
- `env.bytes`
  - Takes an `encoding` keyword argument for indicating how the bytes are encoded.
    For now only `hex` is supported.

### Default values<a name="default-values"></a>

Normally, if an environment variable is not found, typenv raises an exception.
If a default value is provided, however, that will be returned instead of raising.

```python
from typenv import Env

env = Env()

BOOL = env.bool("NON_EXISTING_NAME", default=False)  # => False
LIST = env.list("NON_EXISTING_NAME", default=["a", "b"])  # => ["a", "b"]
OPTIONAL_INT = env.int("NON_EXISTING_NAME", default=None)  # => None
```

### Name prefixes<a name="name-prefixes"></a>

```bash
export FLASK_HOST=127.0.0.1
export FLASK_PORT=44144
```

```python
from typenv import Env

env = Env()

# Explicitly prefixing variable names works, but repeats itself
# (especially given more environment variables and nested prefixes).
HOST = env.str("FLASK_HOST")  # => "127.0.0.1"
PORT = env.int("FLASK_PORT")  # => 44144

# This reads the same variables as above, and can be a nice way of
# reducing repetition and expressing structure. Note that it is possible
# to have nested `with` statements.
with env.prefixed("FLASK_"):
    HOST = env.str("HOST")  # => "127.0.0.1"
    PORT = env.int("PORT")  # => 44144

# For more control, one can mutate `env.prefix` (of type list[str])
# directly. Note that if an exception occurs reading the environment
# variables, then `env.prefix` will not be reset to its initial value,
# which is something that the `with` statement would take care of.
env.prefix.append("FLASK_")
HOST = env.str("HOST")  # => "127.0.0.1"
PORT = env.int("PORT")  # => 44144
env.prefix.pop()
```

### Name character set<a name="name-character-set"></a>

Typenv validates environment variable names.
By default, the set of allowed characters includes upper case ASCII letters, digits and the underscore (`_`).

The set of allowed characters can be configured:

```python
from typenv import Env

env = Env(allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
```

### Name uppercasing<a name="name-uppercasing"></a>

```bash
export UPPER_CASE_NAME=true
```

```python
from typenv import Env

# Environment variable names in type cast methods will automatically be upper
# cased when `upper=True` is set here.
env = Env(upper=True)

NAME = env.bool("upper_casE_Name")
```

### Validation<a name="validation"></a>

```bash
export NAME='Harry Potter'
export AGE=14
```

```python
from typenv import Env

env = Env()

# A single validator function
NAME = env.str("NAME", validate=lambda n: n.startswith("Harry"))


# A validator function can signal error by raising an exception
def is_positive(num):
    if num <= 0:
        raise Exception("Number is not positive")


# A validator function can alternatively return `False` to signal an error
def is_less_than_thousand(num):
    if num >= 1000:
        return False
    return True


# Multiple validator functions can be passed as an iterable of callables
AGE = env.int("AGE", validate=(is_positive, is_less_than_thousand))
```

### Reading from a `.env` file<a name="reading-from-a-env-file"></a>

While developing, it is often useful to read environment variables from a file.
Typenv supports this via the `Env.read_end()` method.
The method will look for a file (by default) named `.env` in current working directory
and import environment variables from it.
If a file is not found,
the method will walk up in the directory tree until a file is found or the root directory is reached.
The method returns a boolean that is `True` if a file is found.

Given a `.env` file in current working directory with the following content

```sh
SOME_VAR='some value'
```

The following code will be able to read and parse the value

```python
from typenv import Env

env = Env()
env.read_env()

SOME_VAR = env.str("SOME_VAR")  # => "some value"
```

### Dumping parsed values<a name="dumping-parsed-values"></a>

```bash
export SOME_STR=blaablaa
export SOME_INT=99
```

```python
from typenv import Env, ParsedValue

env = Env()

SOME_STR = env.str("SOME_STR")
SOME_INT = env.int("SOME_INT")

assert env.dump() == {
    "SOME_INT": ParsedValue(value=99, type="int", optional=False),
    "SOME_STR": ParsedValue(value="blaablaa", type="str", optional=False),
}
```

## Acknowledgments<a name="acknowledgments"></a>

The public API of this library is almost an exact copy of [environs](https://github.com/sloria/environs),
which is based on [envparse](https://github.com/rconradharris/envparse) and [django-environ](https://github.com/joke2k/django-environ).
Credit for the interface goes to the authors of those libraries.
