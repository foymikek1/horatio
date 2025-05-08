# File: tests/ssh_server/integration_specs/conftest.py

import threading
import time
import pytest

from ssh_server.server import start_server, ServerConfig

@pytest.fixture(autouse=True)
def ssh_server(monkeypatch):
    """
    Starts the SSH server in a background thread before each integration test,
    with a minimal config. Tests that need custom behavior (e.g. fault injection
    or different credentials) can still monkeypatch ServerConfig or internals.
    """
    config = ServerConfig(
        program_path="vm_core/tests/programs/load_imm.bin",
        port=2222,
        host_key_path="ssh_server/ssh_host_rsa_key",
        username="lab",
        password="labpass",
        idle_timeout=1.0,
    )

    server_thread = threading.Thread(
        target=start_server,
        args=(config,),
        daemon=True,
    )
    server_thread.start()

    # give the server a moment to bind the socket, load keys, etc.
    time.sleep(0.5)

    yield

    # no explicit teardown needed; thread is daemonized
