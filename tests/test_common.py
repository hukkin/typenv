from decimal import Decimal as D

import pytest

from typenv import Env, ParsedValue


def test_default_to_none(env):
    assert env.int("THIS_IS_NOT_IN_ENV", default=None) is None


def test_missing(env):
    with pytest.raises(Exception) as exc_info:
        env.int("THIS_IS_NOT_IN_ENV")
    assert '"THIS_IS_NOT_IN_ENV" is missing' in exc_info.value.args[0]


def test_empty_str_name(env):
    with pytest.raises(ValueError) as exc_info:
        env.int("")
    assert "Environment variable name can't be empty string" in exc_info.value.args[0]


def test_invalid_char_in_name(env):
    with pytest.raises(ValueError) as exc_info:
        env.int("HERES_AN_INVALID_CHAR_=")
    assert "Environment variable name contains invalid character(s)" in exc_info.value.args[0]


def test_name_starts_with_number(env):
    with pytest.raises(ValueError) as exc_info:
        env.int("7HIS_STARTS_WITH_NUMBER")
    assert "Environment variable name can't start with a number" in exc_info.value.args[0]


def test_upper_casing(set_env):
    set_env({"AN_INTEGER": "982"})
    assert Env(upper=True).int("aN_iNtEgEr") == 982


def test_validators_single(set_env, env):
    def is_positive(val):
        return val > 0

    def is_negative(val):
        return val < 0

    set_env({"AN_INTEGER": "982"})

    assert env.int("AN_INTEGER", validate=is_positive) == 982
    assert env.int("AN_INTEGER", validate=(is_positive, is_positive)) == 982

    with pytest.raises(Exception):
        env.int("AN_INTEGER", validate=is_negative)
    with pytest.raises(Exception):
        env.int("AN_INTEGER", validate=(is_positive, is_negative))


def test_prefix(set_env, env):
    set_env({"PREFIX_STRING": "some string"})
    assert env.str("PREFIX_STRING") == "some string"
    env.prefix.append("PREFIX_")
    assert env.str("STRING") == "some string"
    env.prefix.pop()
    assert env.str("PREFIX_STRING") == "some string"


def test_prefixed(set_env, env):
    set_env({"PF1_PF2_STRING": "some string"})
    assert env.str("PF1_PF2_STRING") == "some string"
    with env.prefixed("PF1_"):
        assert env.str("PF2_STRING") == "some string"
        with env.prefixed("PF2_"):
            assert env.str("STRING") == "some string"
        assert env.str("PF2_STRING") == "some string"
    assert env.str("PF1_PF2_STRING") == "some string"


def test_read_env(env):
    env.read_env("./tests/.env.test")
    assert env.str("A_STRING") == "blabla"


def test_dump_and_get_example(set_env, env):
    set_env(
        {
            "VAR_1": "some string",
            "VAR_2": "4",
            "VAR_3": "4.5",
            "VAR_4": "True,False",
            "EXTRA_VAR": "dont read this",
        }
    )
    env.str("VAR_1", default="some default")
    env.int("VAR_2")
    env.decimal("VAR_3")
    env.list("VAR_4", subcast=bool)
    env.json("NON_EXISTING", default={})
    assert env.dump() == {
        "VAR_1": ParsedValue("some string", "str", True),
        "VAR_2": ParsedValue(4, "int", False),
        "VAR_3": ParsedValue(D("4.5"), "decimal", False),
        "VAR_4": ParsedValue([True, False], "list", False),
        "NON_EXISTING": ParsedValue({}, "json", True),
    }
    assert env.get_example() == (
        "NON_EXISTING=Optional[json]\n"
        "VAR_1=Optional[str]\n"
        "VAR_2=int\n"
        "VAR_3=decimal\n"
        "VAR_4=list\n"
    )
