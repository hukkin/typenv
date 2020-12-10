def test_hex(set_env, env):
    set_env({"HEX_STRING": "01fe"})
    assert env.bytes("HEX_STRING", encoding="hex") == b"\x01\xfe"


def test_hex_prefix(set_env, env):
    set_env({"HEX_STRING": "0x01fe"})
    assert env.bytes("HEX_STRING", encoding="hex") == b"\x01\xfe"


def test_hex_no_leading_zero(set_env, env):
    set_env({"HEX_STRING": "1fe"})
    assert env.bytes("HEX_STRING", encoding="hex") == b"\x01\xfe"
