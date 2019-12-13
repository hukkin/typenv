def test_float(set_env, env):
    set_env({"INT": "2", "FLOAT": "2.0", "MISSING_0": ".21"})
    assert env.float("INT") == 2.0
    assert env.float("FLOAT") == 2.0
    assert env.float("MISSING_0") == 0.21
