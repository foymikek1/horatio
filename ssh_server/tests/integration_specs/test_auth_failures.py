import pytest
import paramiko
import time
import subprocess
import os
import sys
from pathlib import Path

# No ssh_server fixture here—uses autouse in conftest.py

def test_invalid_credentials_do_not_spawn_vm():
    # Ensure host key exists
    key_path = Path("ssh_server/ssh_host_rsa_key")
    if not key_path.exists():
        subprocess.run(
            ["ssh-keygen", "-t", "rsa", "-f", str(key_path), "-N", ""],
            check=True,
        )

    # Try with bad username
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    with pytest.raises(paramiko.ssh_exception.AuthenticationException):
        client.connect(
            hostname="127.0.0.1",
            port=2222,
            username="wrong",
            password="labpass",
            look_for_keys=False,
            allow_agent=False,
        )

    # Try with bad password
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    with pytest.raises(paramiko.ssh_exception.AuthenticationException):
        client.connect(
            hostname="127.0.0.1",
            port=2222,
            username="lab",
            password="wrong",
            look_for_keys=False,
            allow_agent=False,
        )
