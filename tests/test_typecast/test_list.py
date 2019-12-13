def test_list(set_env, env):
    set_env({"VALID_LIST": "one item,another item,3rd item"})
    assert env.list("VALID_LIST") == ["one item", "another item", "3rd item"]
