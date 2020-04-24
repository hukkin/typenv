import pytest


def test_bool_trues(set_env, env):
    set_env({"VAR1": "1", "VAR2": "true", "VAR3": "True", "VAR4": "tRuE"})
    assert env.bool("VAR1") is True
    assert env.bool("VAR2") is True
    assert env.bool("VAR3") is True
    assert env.bool("VAR4") is True


def test_bool_falses(set_env, env):
    set_env({"VAR1": "0", "VAR2": "false", "VAR3": "False", "VAR4": "fAlSe"})
    assert env.bool("VAR1") is False
    assert env.bool("VAR2") is False
    assert env.bool("VAR3") is False
    assert env.bool("VAR4") is False


def test_bool_invalid(set_env, env):
    set_env({"NON_BOOL": "notbool"})
    with pytest.raises(Exception) as exc_info:
        env.bool("NON_BOOL")
    err_msg = str(exc_info.value)
    assert "Failed to cast" in err_msg
    assert "notbool" in err_msg
    assert "NON_BOOL" in err_msg
