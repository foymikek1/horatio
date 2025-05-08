from pathlib import Path
import pytest
from ssh_server import hostkey


def test_load_valid_host_key(tmp_path):
    # Generate and write a temporary RSA key for testing
    key_path = tmp_path / "test_rsa_key"
    key = hostkey.paramiko.RSAKey.generate(1024)
    key.write_private_key_file(str(key_path))

    loaded = hostkey.load_host_key(str(key_path))
    assert loaded.get_name() == "ssh-rsa"


def test_load_host_key_missing_file():
    # Ensure we raise a FileNotFoundError if the key path is bad
    with pytest.raises(FileNotFoundError):
        hostkey.load_host_key("/nonexistent/key/path")
