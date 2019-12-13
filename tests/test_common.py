import pytest

from typenv import Env


def test_default_to_none(env):
    assert env.int("THIS_IS_NOT_IN_ENV", default=None) is None


def test_missing(env):
    with pytest.raises(Exception) as exc_info:
        env.int("THIS_IS_NOT_IN_ENV")
    assert "Mandatory environment variable is missing" in exc_info.value.args[0]


def test_empty_str_name(env):
    with pytest.raises(Exception) as exc_info:
        env.int("")
    assert "Environment variable name can't be empty string" in exc_info.value.args[0]


def test_invalid_char_in_name(env):
    with pytest.raises(Exception) as exc_info:
        env.int("HERES_AN_INVALID_CHAR_=")
    assert "Environment variable name contains invalid character(s)" in exc_info.value.args[0]


def test_name_starts_with_number(env):
    with pytest.raises(Exception) as exc_info:
        env.int("7HIS_STARTS_WITH_NUMBER")
    assert "Environment variable name can't start with a number" in exc_info.value.args[0]


def test_upper_casing(set_env):
    set_env({"AN_INTEGER": "982"})
    assert Env(upper=True).int("aN_iNtEgEr") == 982


# TODO: test_prefix
# TODO: test read_env
