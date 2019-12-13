import pytest

from typenv import Env


@pytest.fixture
def env():
    return Env()


@pytest.fixture
def set_env(monkeypatch):
    def _set_env(env_map):
        for k, v in env_map.items():
            monkeypatch.setenv(k, v)

    return _set_env


def test_int(set_env, env):
    set_env({"AN_INTEGER": "982"})
    assert env.int("AN_INTEGER") == 982


def test_int_invalid(set_env, env):
    set_env({"AN_INTEGER": "982.1"})
    with pytest.raises(ValueError) as exc_info:
        env.int("AN_INTEGER")
    assert "invalid literal for int()" in exc_info.value.args[0]


def test_int_default(env):
    assert env.int("THIS_IS_NOT_IN_ENV", default=12) == 12


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


def test_json(set_env, env):
    set_env(
        {"VALID_JSON": '{"a": "x", "b": 1.2, "c": true, "d": null, "e": [2,3], "f": {"g": 0}}'}
    )
    assert env.json("VALID_JSON") == {
        "a": "x",
        "b": 1.2,
        "c": True,
        "d": None,
        "e": [2, 3],
        "f": {"g": 0},
    }
