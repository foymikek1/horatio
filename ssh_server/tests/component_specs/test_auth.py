# File: tests/ssh_server/component_specs/test_auth.py

import os
import sys
import time
import subprocess
from pathlib import Path

import paramiko
import pytest

def test_accepts_login_with_valid_credentials(tmp_path):
    key_path = Path("ssh_server/ssh_host_rsa_key")
    if not key_path.exists():
        subprocess.run(
            ["ssh-keygen", "-t", "rsa", "-f", str(key_path), "-N", ""],
            check=True,
        )

    # Build minimal valid program: LOAD A, 42; HALT
    prog = tmp_path / "prog.bin"
    prog.write_bytes(b"\x01\x2A\xFF")

    proc = subprocess.Popen(
        [sys.executable, "ssh_server/server.py", str(prog)],
        env={**os.environ, "PYTHONPATH": "."},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(1.0)

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname="127.0.0.1",
            port=2222,
            username="lab",
            password="lab",
            look_for_keys=False,
            allow_agent=False,
        )

        chan = client.invoke_shell()
        chan.settimeout(2.0)

        output = b""
        while True:
            try:
                chunk = chan.recv(1024)
                if not chunk:
                    break
                output += chunk
                if b"RUNNING = 0" in output:
                    break
            except Exception:
                break

        # we expect the VM to print the register contents, including A=42
        assert b"A = 42" in output

    finally:
        proc.terminate()
        client.close()

def test_rejects_login_with_invalid_credentials(tmp_path):
    # similar to above, but wrong password → should fail to authenticate
    key_path = Path("ssh_server/ssh_host_rsa_key")
    if not key_path.exists():
        subprocess.run(
            ["ssh-keygen", "-t", "rsa", "-f", str(key_path), "-N", ""],
            check=True,
        )

    prog = tmp_path / "prog.bin"
    prog.write_bytes(b"\x01\x2A\xFF")

    proc = subprocess.Popen(
        [sys.executable, "ssh_server/server.py", str(prog)],
        env={**os.environ, "PYTHONPATH": "."},
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(1.0)

    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        with pytest.raises(paramiko.ssh_exception.AuthenticationException):
            client.connect(
                hostname="127.0.0.1",
                port=2222,
                username="lab",
                password="wrongpass",
                look_for_keys=False,
                allow_agent=False,
            )
    finally:
        proc.terminate()
