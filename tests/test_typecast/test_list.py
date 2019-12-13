def test_list(set_env, env):
    set_env({"VALID_LIST": "one item,another item,3rd item"})
    assert env.list("VALID_LIST") == ["one item", "another item", "3rd item"]


def test_list_subcast_bool(set_env, env):
    set_env({"BOOL_LIST": "1,false,true,FaLSE,0"})
    assert env.list("BOOL_LIST", subcast=bool) == [True, False, True, False, False]
