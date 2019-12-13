def test_str(set_env, env):
    set_env({"A_STRING": "some string"})
    assert env.str("A_STRING") == "some string"
