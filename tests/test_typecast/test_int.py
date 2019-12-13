import pytest


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
