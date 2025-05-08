import importlib
import os
import pytest

from ssh_server import config


def test_config_defaults():
    config_dict = config.load_config()
    assert config_dict["username"] == "lab"
    assert config_dict["password"] == "lab"
    assert config_dict["port"] == 2222


def test_config_env_override(monkeypatch):
    monkeypatch.setenv("SSH_USER", "admin")
    monkeypatch.setenv("SSH_PASS", "secret")
    monkeypatch.setenv("SSH_PORT", "2300")

    importlib.reload(config)
    config_dict = config.load_config()
    assert config_dict["username"] == "admin"
    assert config_dict["password"] == "secret"
    assert config_dict["port"] == 2300


def test_config_invalid_port(monkeypatch):
    monkeypatch.setenv("SSH_PORT", "not-a-number")

    importlib.reload(config)
    config_dict = config.load_config()
    assert config_dict["port"] == 2222
