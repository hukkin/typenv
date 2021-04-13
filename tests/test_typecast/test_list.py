def test_list(set_env, env):
    set_env({"VALID_LIST": "one item,another item,3rd item"})
    assert env.list("VALID_LIST") == ["one item", "another item", "3rd item"]


def test_list_empty(set_env, env):
    set_env({"EMPTY_LIST": ""})
    assert env.list("EMPTY_LIST") == []


def test_list_subcast_bool(set_env, env):
    set_env({"BOOL_LIST": "TRUE,false,true,FaLSE,FALSE"})
    assert env.list("BOOL_LIST", subcast=bool) == [True, False, True, False, False]
