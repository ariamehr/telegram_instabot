import importlib
import sys
import types


def test_loads_env_variables(monkeypatch):
    # Provide a minimal stub for the dotenv module
    fake_dotenv = types.ModuleType("dotenv")
    fake_dotenv.load_dotenv = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "dotenv", fake_dotenv)

    monkeypatch.setenv("TELEGRAM_TOKEN", "token123")
    monkeypatch.setenv("INSTAGRAM_USER", "user123")
    monkeypatch.setenv("INSTAGRAM_PASSWORD", "pass123")
    monkeypatch.setenv("SESSION_DIR", "my_sessions")

    # Reload config after setting env vars and stubbing dotenv
    config = importlib.import_module("config")
    importlib.reload(config)

    assert config.TELEGRAM_TOKEN == "token123"
    assert config.INSTAGRAM_USER == "user123"
    assert config.INSTAGRAM_PASSWORD == "pass123"
    assert config.SESSION_DIR == "my_sessions"
