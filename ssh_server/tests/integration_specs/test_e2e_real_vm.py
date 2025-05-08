# File: tests/ssh_server/integration_specs/test_e2e_real_vm.py

import os
import sys
import time
from pathlib import Path

import paramiko
import pytest

def test_bytecode_run_e2e(tmp_path):
    """
    Write a minimal bytecode file, send it over SSH, and assert the real VM
    produces the expected output.
    """
    # create a simple bytecode file, e.g. single opcode 0x00 that prints "OK\n"
    bc = tmp_path / "prog.bin"
    bc.write_bytes(b"\x00")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname="localhost",
        port=2222,
        username="lab",
        password="labpass",
        look_for_keys=False,
        allow_agent=False,
    )

    chan = client.invoke_shell()
    chan.settimeout(2.0)

    # send the bytecode payload
    chan.send(bc.read_bytes() + b"\n")

    # read VM output
    out = b""
    deadline = time.time() + 2
    while time.time() < deadline and not out.endswith(b"OK\n"):
        if chan.recv_ready():
            out += chan.recv(1024)
        else:
            time.sleep(0.05)

    chan.close()
    client.close()

    assert out.endswith(b"OK\n")
