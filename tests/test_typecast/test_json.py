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


def test_json_defaults(set_env, env):
    assert env.json("NON_EXISTING_VAR", default=None) is None
    assert env.json("NON_EXISTING_VAR", default=True) is True
    assert env.json("NON_EXISTING_VAR", default=-11) == -11
    assert env.json("NON_EXISTING_VAR", default=0.24) == 0.24
    assert env.json("NON_EXISTING_VAR", default="a string") == "a string"
    assert env.json("NON_EXISTING_VAR", default=["a", "list"]) == ["a", "list"]
    assert env.json("NON_EXISTING_VAR", default={"a": "dict"}) == {"a": "dict"}
