import contextlib
from decimal import Decimal as D
import json
import os
import string
import typing
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    NamedTuple,
    Optional,
    Type,
    TypeVar,
    Union,
)

import dotenv

__version__ = "0.0.2"  # DO NOT EDIT THIS LINE MANUALLY. LET bump2version UTILITY DO IT

# Make aliases for these types because typecast method names shadow the names
_Str = str
_Int = int
_Bool = bool
_Float = float

_T = TypeVar("_T")
_JSONType = Union[None, bool, int, float, str, list, dict]


class _Missing:
    """A type used as a unique object used to signal missing env variable.

    Should not be instantiated
    """


_DEFAULT_NAME_CHARS = string.ascii_uppercase + string.digits + "_"


class ParsedValue(NamedTuple):
    value: Any
    type: str
    optional: bool


def _cast_bool(value: _Str) -> _Bool:
    if value.lower() in {"true", "1"}:
        return True
    if value.lower() in {"false", "0"}:
        return False
    raise Exception("Failed to cast to bool")


def _cast_list(value: _Str, subcast: Callable = _Str) -> List:
    if not value:
        return []
    return [subcast(item) for item in value.split(",")]


# Functions that cast a string to a type
_typecast_map: Dict[str, Callable] = {
    "bool": _cast_bool,
    "decimal": D,
    "float": float,
    "int": int,
    "json": json.loads,
    "list": _cast_list,
    "str": str,
}


class Env:
    def __init__(
        self, *, allowed_chars: Iterable[_Str] = _DEFAULT_NAME_CHARS, upper: _Bool = False,
    ):
        self._allowed_chars = allowed_chars
        self._upper = upper
        self.prefix: List[_Str] = []
        self._parsed: Dict[str, ParsedValue] = {}

    def _get_and_cast(
        self,
        name: _Str,
        cast_type: _Str,
        default: Union[Type[_Missing], None, _T],
        validate: Union[Callable, Iterable[Callable]],
        *,
        typecast_kwds: Dict[str, Any] = None,
    ) -> Optional[_T]:
        if typecast_kwds is None:
            typecast_kwds = {}

        is_optional = default is not _Missing

        name = self._preprocess_name(name)

        value = os.environ.get(name, default)

        if value is _Missing:
            raise Exception("Mandatory environment variable is missing")
        assert not isinstance(value, type), "Value cant be any other type besides _Missing"

        if value is None:
            self._parsed[name] = ParsedValue(value, cast_type, is_optional)
            return value

        if isinstance(value, _Str):
            value = _typecast_map[cast_type](value, **typecast_kwds)

        self._validate(value, validate)

        self._parsed[name] = ParsedValue(value, cast_type, is_optional)
        # Ignore type checker. The typecast that assigns Any to `value` makes it
        # very hard to prove that `value` is of type `_T`.
        return value  # type: ignore

    @typing.overload
    def str(self, name: _Str, *, default: Union[Type[_Missing], _Str] = _Missing,) -> _Str:
        ...

    @typing.overload
    def str(self, name: _Str, *, default: None = None,) -> Optional[_Str]:
        ...

    def str(
        self,
        name: _Str,
        *,
        default: Union[Type[_Missing], None, _Str] = _Missing,
        validate: Union[Callable, Iterable[Callable]] = (),
    ) -> Optional[_Str]:
        return self._get_and_cast(name, "str", default, validate)

    @typing.overload
    def int(self, name: _Str, *, default: Union[Type[_Missing], _Int] = _Missing) -> _Int:
        ...

    @typing.overload
    def int(self, name: _Str, *, default: None = None,) -> Optional[_Int]:
        ...

    def int(
        self,
        name: _Str,
        *,
        default: Union[Type[_Missing], None, _Int] = _Missing,
        validate: Union[Callable, Iterable[Callable]] = (),
    ) -> Optional[_Int]:
        return self._get_and_cast(name, "int", default, validate)

    @typing.overload
    def bool(self, name: _Str, *, default: Union[Type[_Missing], _Bool] = _Missing) -> _Bool:
        ...

    @typing.overload
    def bool(self, name: _Str, *, default: None = None,) -> Optional[_Bool]:
        ...

    def bool(
        self,
        name: _Str,
        *,
        default: Union[Type[_Missing], None, _Bool] = _Missing,
        validate: Union[Callable, Iterable[Callable]] = (),
    ) -> Optional[_Bool]:
        return self._get_and_cast(name, "bool", default, validate)

    @typing.overload
    def float(self, name: _Str, *, default: Union[Type[_Missing], _Float] = _Missing) -> _Float:
        ...

    @typing.overload
    def float(self, name: _Str, *, default: None = None,) -> Optional[_Float]:
        ...

    def float(
        self,
        name: _Str,
        *,
        default: Union[Type[_Missing], None, _Float] = _Missing,
        validate: Union[Callable, Iterable[Callable]] = (),
    ) -> Optional[_Float]:
        return self._get_and_cast(name, "float", default, validate)

    @typing.overload
    def decimal(self, name: _Str, *, default: Union[Type[_Missing], D] = _Missing) -> D:
        ...

    @typing.overload
    def decimal(self, name: _Str, *, default: None = None,) -> Optional[D]:
        ...

    def decimal(
        self,
        name: _Str,
        *,
        default: Union[Type[_Missing], None, D] = _Missing,
        validate: Union[Callable, Iterable[Callable]] = (),
    ) -> Optional[D]:
        return self._get_and_cast(name, "decimal", default, validate)

    def json(
        self,
        name: _Str,
        *,
        default: Union[Type[_Missing], None, _JSONType] = _Missing,
        validate: Union[Callable, Iterable[Callable]] = (),
    ) -> Any:
        value = self._get_and_cast(name, "json", default, validate)
        # Extra validation: make sure user provided default serializes to json
        json.dumps(value)
        return value

    @typing.overload
    def list(
        self, name: _Str, *, default: Union[Type[_Missing], List[_T]] = _Missing
    ) -> List[_Str]:
        ...

    @typing.overload
    def list(self, name: _Str, *, default: None = None) -> Optional[List[_Str]]:
        ...

    @typing.overload
    def list(
        self,
        name: _Str,
        *,
        default: Union[Type[_Missing], List[_T]] = _Missing,
        subcast: Callable[..., _T],
    ) -> List[_T]:
        ...

    @typing.overload
    def list(
        self, name: _Str, *, default: None = None, subcast: Callable[..., _T]
    ) -> Optional[List[_T]]:
        ...

    def list(
        self,
        name: _Str,
        *,
        default: Union[Type[_Missing], None, List[_T]] = _Missing,
        validate: Union[Callable, Iterable[Callable]] = (),
        subcast: Callable = _Str,
    ) -> Optional[List]:
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

    def __contains__(self, item: _Str) -> _Bool:
        raise NotImplementedError

    @staticmethod
    def read_env(path: _Str = ".env", override: _Bool = False) -> _Bool:
        """If path is a file, load it to ENV.

        If not, recursively walk up in dir tree and look for a file with
        that name, starting from CWD
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

    def dump(self) -> Dict[_Str, ParsedValue]:
        return self._parsed

    def _preprocess_name(self, name: _Str) -> _Str:
        name = "".join(self.prefix) + name

        if self._upper:
            name = name.upper()
        self._validate_name(name)
        return name

    @staticmethod
    def _validate(value: Any, validators: Union[Callable, Iterable[Callable]]) -> None:
        if callable(validators):
            validators = (validators,)
        for validator in validators:
            validator_result = validator(value)
            if validator_result is False:
                raise Exception("A value did not pass custom validation")

    def _validate_name(self, name: _Str) -> None:
        if not name:
            raise Exception("Environment variable name can't be empty string")
        if not all(c in self._allowed_chars for c in name):
            raise Exception("Environment variable name contains invalid character(s)")
        if name[0].isdigit():
            raise Exception("Environment variable name can't start with a number")
