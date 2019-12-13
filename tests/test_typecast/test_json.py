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
