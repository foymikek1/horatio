import pytest
import paramiko
import threading
import time
from pathlib import Path

from ssh_server.server import ServerConfig, start_server

# No ssh_server fixture here—uses autouse in conftest.py

def test_vm_crash_closes_channel(monkeypatch, tmp_path):
    # Create a tiny program (just HALT)
    prog = tmp_path / "halt.bin"
    prog.write_bytes(b"\xFF")

    # Monkey-patch Popen so the VM “crashes” immediately
    class FakePopen:
        def __init__(*args, **kwargs):
            pass
        def poll(self):
            return 0  # exited immediately
        @property
        def stdout(self):
            return b""
    monkeypatch.setattr("ssh_server.server.subprocess", FakePopen)

    # Launch our server in a thread using default creds
    config = ServerConfig(
        program_path=str(prog),
        port=2222,
        host_key_path="ssh_server/ssh_host_rsa_key",
        username="lab",
        password="labpass",
        idle_timeout=1.0,
    )
    server_thread = threading.Thread(target=start_server, args=(config,), daemon=True)
    server_thread.start()
    time.sleep(0.5)

    # Connect and open a shell; it should immediately tear down the channel
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        "127.0.0.1",
        port=2222,
        username="lab",
        password="labpass",
        look_for_keys=False,
        allow_agent=False,
    )
    chan = client.invoke_shell()

    with pytest.raises(paramiko.SSHException):
        # Any attempt to send/receive should raise now
        chan.send(b"ping")
        chan.recv(1024)
