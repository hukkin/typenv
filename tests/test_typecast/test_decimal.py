from decimal import Decimal as D


def test_decimal(set_env, env):
    set_env({"INT": "2", "FLOAT": "2.0", "MISSING_0": ".21"})
    assert isinstance(env.decimal("INT"), D)
    assert env.decimal("INT") == D(2)
    assert isinstance(env.decimal("FLOAT"), D)
    assert env.decimal("FLOAT") == D("2.0")
    assert isinstance(env.decimal("MISSING_0"), D)
    assert env.decimal("MISSING_0") == D(".21")
