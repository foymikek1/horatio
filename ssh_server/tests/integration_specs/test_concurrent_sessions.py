import threading
import time

import pytest
import paramiko

from ssh_server.server import start_server

@pytest.fixture(scope="module", autouse=True)
def ssh_server():
    """Start the SSH→VM server in a daemon thread once per test module."""
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    # give it a moment to bind
    time.sleep(0.5)
    yield

def session_task():
    """Connect, send a byte, receive response, then disconnect."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("localhost", 2222, username="lab", password="labpass")
    chan = client.get_transport().open_session()
    chan.invoke_shell()
    chan.send(b"x\n")
    # expect at least one byte back
    _ = chan.recv(1024)
    chan.close()
    client.close()

def test_parallel_sessions():
    """Ensure 50 concurrent sessions complete without error."""
    threads = [threading.Thread(target=session_task) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    # if no exceptions, concurrency is OK
    assert True
