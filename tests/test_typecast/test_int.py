import pytest


def test_int(set_env, env):
    set_env({"AN_INTEGER": "982"})
    assert env.int("AN_INTEGER") == 982


def test_int_invalid(set_env, env):
    set_env({"AN_INTEGER": "982.1"})
    with pytest.raises(Exception) as exc_info:
        env.int("AN_INTEGER")
    err_msg = str(exc_info.value)
    assert "Failed to cast" in err_msg
    assert "int" in err_msg
    assert "AN_INTEGER" in err_msg
    assert "982.1" in err_msg


def test_int_default(env):
    assert env.int("THIS_IS_NOT_IN_ENV", default=12) == 12
