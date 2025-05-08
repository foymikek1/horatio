# File: tests/ssh_server/integration_specs/test_large_payload.py

import time

import paramiko

def test_large_data_stream():
    """Send and receive a ~100KB payload without loss or deadlock."""
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
    chan.settimeout(5.0)

    big = b"A" * 100_000 + b"\n"
    chan.send(big)

    received = bytearray()
    deadline = time.time() + 5
    while time.time() < deadline and len(received) < len(big):
        if chan.recv_ready():
            received.extend(chan.recv(4096))
        else:
            time.sleep(0.05)

    chan.close()
    client.close()

    assert received == big
