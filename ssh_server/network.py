import socket
from typing import Tuple

def create_socket(port: int) -> socket.socket:
    """
    Create, bind and listen on a localhost-only TCP socket.
    Raises if the port is in use.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # only bind to localhost for safety
    sock.bind(("127.0.0.1", port))
    sock.listen(5)
    return sock
