import threading
import time

import pytest
import paramiko

from ssh_server.server import start_server

# requires handle_connection to implement an idle timeout (e.g. 5s)
@pytest.fixture(scope="module", autouse=True)
def ssh_server():
    t = threading.Thread(target=start_server, daemon=True)
    t.start()
    time.sleep(0.5)
    yield

def test_idle_disconnect():
    """Session with no activity must close after timeout."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect("localhost", 2222, "lab", "labpass")
    chan = client.get_transport().open_session()
    chan.invoke_shell()

    # wait longer than configured idle timeout (e.g. 5s)
    time.sleep(6)
    assert chan.closed
    client.close()
