import pytest

from typenv import Env


@pytest.fixture
def env():
    return Env()


@pytest.fixture
def set_env(monkeypatch):
    def _set_env(env_map):
        for k, v in env_map.items():
            monkeypatch.setenv(k, v)

    return _set_env
