from __future__ import annotations

__version__ = "0.2.0"  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT

from collections.abc import Callable, Generator, Iterable, Mapping
import contextlib
from decimal import Decimal as D
import json
import os
import string
import sys
from types import MappingProxyType
import typing
from typing import Any, NamedTuple, TypeVar, Union

import dotenv

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal


_EMPTY_MAP: MappingProxyType = MappingProxyType({})

# Make aliases for these types because typecast method names in `Env` class
# shadow the names. Note that these aliases only need to be used within the
# `Env` class scope
_Str = str
_Int = int
_Bool = bool
_Float = float
_Bytes = bytes
_List = list

_T = TypeVar("_T")
# TODO: Use the "|" operator when minimum Python version is 3.10
_JSONType = Union[None, bool, int, float, str, list, dict]


class _Missing:
    """A type used as a unique object to signal a missing env variable.

    Should not be instantiated.
    """


_DEFAULT_NAME_CHARS = string.ascii_uppercase + string.digits + "_"


class ParsedValue(NamedTuple):
    value: Any
    type: str
    optional: bool


def _cast_bool(value: str) -> bool:
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    raise Exception(f'Failed to cast value "{value}" to bool')


def _cast_list(value: str, subcast: Callable = str) -> list:
    if value == "":
        return []
    return [subcast(item) for item in value.split(",")]


def _cast_bytes(value: str) -> bytes:
    """Cast a string to bytes.

    For now this only deals with hex encoded strings.
    """
    value = value.lower()
    value = _removeprefix(value, "0x")
    if len(value) % 2:
        value = "0" + value
    return bytes.fromhex(value)


# Functions that cast a string to a type
_typecast_map: Mapping[str, Callable] = {
    "bool": _cast_bool,
    "decimal": D,
    "float": float,
    "int": int,
    "json": json.loads,
    "list": _cast_list,
    "str": str,
    "bytes": _cast_bytes,
}


class Env:
    def __init__(
        self, *, allowed_chars: Iterable[_Str] = _DEFAULT_NAME_CHARS, upper: _Bool = False
    ):
        self._allowed_chars = allowed_chars
        self._upper = upper
        self.prefix: _List[_Str] = []
        self._parsed: dict[_Str, ParsedValue] = {}

    def _get_and_cast(
        self,
        name: _Str,
        cast_type: _Str,
        default: type[_Missing] | None | _T,
        validate: Callable | Iterable[Callable],
        *,
        typecast_kwds: Mapping[_Str, Any] = _EMPTY_MAP,
    ) -> _T | None:
        is_optional = default is not _Missing

        name = self._preprocess_name(name)

        try:
            uncast_value = os.environ[name]
        except KeyError:
            if default is _Missing:
                raise Exception(f'Mandatory environment variable "{name}" is missing')
            if default is None:
                self._parsed[name] = ParsedValue(None, cast_type, is_optional)
                return None
            value = default
        else:
            try:
                value = _typecast_map[cast_type](uncast_value, **typecast_kwds)
            except Exception as e:
                raise Exception(
                    f'Failed to cast "{uncast_value}" (variable name "{name}") to {cast_type}'
                ) from e

        self._validate(name, value, validate)
        self._parsed[name] = ParsedValue(value, cast_type, is_optional)
        # Ignore type checker. The typecast above assigns a value of `Any` type
        # to `value` making it very hard to prove that `value` is of type `_T`.
        return value  # type: ignore

    @typing.overload
    def str(
        self,
        name: _Str,
        *,
        default: type[_Missing] | _Str = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Str:
        ...

    @typing.overload
    def str(
        self, name: _Str, *, default: None, validate: Callable | Iterable[Callable] = ()
    ) -> _Str | None:
        ...

    def str(
        self,
        name: _Str,
        *,
        default: type[_Missing] | None | _Str = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Str | None:
        return self._get_and_cast(name, "str", default, validate)

    @typing.overload
    def bytes(
        self,
        name: _Str,
        *,
        encoding: Literal["hex"],
        default: type[_Missing] | _Bytes = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Bytes:
        ...

    @typing.overload
    def bytes(
        self,
        name: _Str,
        *,
        encoding: Literal["hex"],
        default: None,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Bytes | None:
        ...

    def bytes(
        self,
        name: _Str,
        *,
        encoding: Literal["hex"],
        default: type[_Missing] | None | _Bytes = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Bytes | None:
        return self._get_and_cast(name, "bytes", default, validate)

    @typing.overload
    def int(
        self,
        name: _Str,
        *,
        default: type[_Missing] | _Int = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Int:
        ...

    @typing.overload
    def int(
        self, name: _Str, *, default: None, validate: Callable | Iterable[Callable] = ()
    ) -> _Int | None:
        ...

    def int(
        self,
        name: _Str,
        *,
        default: type[_Missing] | None | _Int = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Int | None:
        return self._get_and_cast(name, "int", default, validate)

    @typing.overload
    def bool(
        self,
        name: _Str,
        *,
        default: type[_Missing] | _Bool = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Bool:
        ...

    @typing.overload
    def bool(
        self, name: _Str, *, default: None, validate: Callable | Iterable[Callable] = ()
    ) -> _Bool | None:
        ...

    def bool(
        self,
        name: _Str,
        *,
        default: type[_Missing] | None | _Bool = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Bool | None:
        return self._get_and_cast(name, "bool", default, validate)

    @typing.overload
    def float(
        self,
        name: _Str,
        *,
        default: type[_Missing] | _Float = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Float:
        ...

    @typing.overload
    def float(
        self, name: _Str, *, default: None, validate: Callable | Iterable[Callable] = ()
    ) -> _Float | None:
        ...

    def float(
        self,
        name: _Str,
        *,
        default: type[_Missing] | None | _Float = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _Float | None:
        return self._get_and_cast(name, "float", default, validate)

    @typing.overload
    def decimal(
        self,
        name: _Str,
        *,
        default: type[_Missing] | D = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> D:
        ...

    @typing.overload
    def decimal(
        self, name: _Str, *, default: None, validate: Callable | Iterable[Callable] = ()
    ) -> D | None:
        ...

    def decimal(
        self,
        name: _Str,
        *,
        default: type[_Missing] | None | D = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> D | None:
        return self._get_and_cast(name, "decimal", default, validate)

    def json(
        self,
        name: _Str,
        *,
        default: type[_Missing] | None | _JSONType = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> Any:
        value = self._get_and_cast(name, "json", default, validate)
        # Extra validation: make sure user provided default serializes to json
        json.dumps(value)
        return value

    @typing.overload
    def list(
        self,
        name: _Str,
        *,
        default: type[_Missing] | _List = _Missing,
        validate: Callable | Iterable[Callable] = (),
    ) -> _List[_Str]:
        ...

    @typing.overload
    def list(
        self, name: _Str, *, default: None, validate: Callable | Iterable[Callable] = ()
    ) -> _List[_Str] | None:
        ...

    @typing.overload
    def list(
        self,
        name: _Str,
        *,
        default: type[_Missing] | _List[_T] = _Missing,
        validate: Callable | Iterable[Callable] = (),
        subcast: Callable[..., _T],
    ) -> _List[_T]:
        ...

    @typing.overload
    def list(
        self,
        name: _Str,
        *,
        default: None,
        validate: Callable | Iterable[Callable] = (),
        subcast: Callable[..., _T],
    ) -> _List[_T] | None:
        ...

    def list(
        self,
        name: _Str,
        *,
        default: type[_Missing] | None | _List[_T] = _Missing,
        validate: Callable | Iterable[Callable] = (),
        subcast: Callable = _Str,
    ) -> _List | None:
        assert subcast in {_Str, _Int, _Bool, _Float, D}
        # Do lower() so that "Decimal" converts to "decimal"
        subcast_func = _typecast_map[subcast.__name__.lower()]
        return self._get_and_cast(
            name, "list", default, validate, typecast_kwds={"subcast": subcast_func}
        )

    @contextlib.contextmanager
    def prefixed(self, prefix: _Str) -> Generator[None, None, None]:
        old_prefix = self.prefix.copy()
        self.prefix.append(prefix)
        try:
            yield
        finally:
            self.prefix = old_prefix

    @staticmethod
    def read_env(path: _Str = ".env", override: _Bool = False) -> _Bool:
        """Load environment variables from a file.

        If `path` is a file, load it to ENV. If not, recursively walk up
        in dir tree and look for a file with that name, starting from
        current working directory. Return a bool representing whether a
        file was found.
        """
        if not os.path.isfile(path):
            path = dotenv.find_dotenv(path, usecwd=True)
            if not path:
                return False
        dotenv.load_dotenv(path, override=override)
        return True

    def get_example(self) -> _Str:
        env_example = ""
        for k, v in sorted(self.dump().items()):
            value_example = v.type
            if v.optional:
                value_example = f"Optional[{value_example}]"
            env_example += f"{k}={value_example}\n"
        return env_example

    def dump(self) -> dict[_Str, ParsedValue]:
        return self._parsed.copy()

    def _preprocess_name(self, name: _Str) -> _Str:
        name = "".join(self.prefix) + name

        if self._upper:
            name = name.upper()
        self._validate_name(name)
        return name

    @staticmethod
    def _validate(name: _Str, value: Any, validators: Callable | Iterable[Callable]) -> None:
        if callable(validators):
            validators = (validators,)

        exc_to_raise = Exception(
            f'Invalid value for "{name}": Value did not pass custom validator'
        )
        for validator in validators:
            try:
                validator_result = validator(value)
            except Exception as e:
                raise exc_to_raise from e
            if validator_result is False:
                raise exc_to_raise

    def _validate_name(self, name: _Str) -> None:
        if not name:
            raise ValueError(
                'Invalid name "": Environment variable name can not be an empty string'
            )
        if any(c not in self._allowed_chars for c in name):
            raise ValueError(
                f'Invalid name "{name}": Environment variable name contains invalid character(s)'
            )
        if name[0].isdigit():
            raise ValueError(
                f'Invalid name "{name}": Environment variable name can not start with a number'
            )


# TODO: replace this with stdlib implementation once min Python version
#       is 3.9
def _removeprefix(string: str, prefix: str) -> str:
    if prefix and string.startswith(prefix):
        return string[len(prefix) :]
    return string
