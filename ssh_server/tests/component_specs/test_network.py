import socket
import pytest
from ssh_server import network


def test_bind_socket_to_localhost():
    sock = network.create_socket(port=0)  # use OS-assigned port
    host, assigned_port = sock.getsockname()

    assert host in ("127.0.0.1", "localhost")  # platform may normalize
    assert assigned_port > 0

    sock.close()


def test_socket_port_already_in_use():
    sock1 = network.create_socket(port=2222)

    with pytest.raises(OSError):
        network.create_socket(port=2222)  # should fail: port already bound

    sock1.close()

