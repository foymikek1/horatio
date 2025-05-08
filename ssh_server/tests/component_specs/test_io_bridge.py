# File: tests/ssh_server/component_specs/test_io_bridge.py

import os
import sys
import time
import subprocess
from pathlib import Path

import paramiko

def test_vm_dev_io_bridge(tmp_path):
    # Same LOAD A, 42; HALT program
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

        assert b"A = 42" in output

    finally:
        proc.terminate()
