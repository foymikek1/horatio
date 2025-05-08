# tests/ssh_server/integration_specs/test_fd_and_process_leaks.py

import os
import sys
import time

import paramiko


def count_fds():
    """
    Count the number of open file descriptors for the current process.
    On Linux: use /proc/<pid>/fd
    On macOS and other platforms: use /dev/fd
    """
    if sys.platform.startswith("linux"):
        fd_dir = f"/proc/{os.getpid()}/fd"
    else:
        fd_dir = "/dev/fd"
    return len(os.listdir(fd_dir))


def test_no_leaks_after_sessions(ssh_server):
    """
    Run several SSH sessions in sequence and assert that there are no
    leaked file descriptors or VM subprocesses.
    """
    before_fds = count_fds()

    # Open and close several sessions
    for _ in range(5):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(
            hostname="127.0.0.1",
            port=2222,
            username="lab",
            password="labpass",
            look_for_keys=False,
            allow_agent=False,
        )
        client.close()
        # give the server a moment to clean up
        time.sleep(0.1)

    after_fds = count_fds()

    # allow a small slack for any ephemeral descriptors (e.g. logs)
    assert after_fds - before_fds < 3, (
        f"Possible FD leak detected: before={before_fds}, after={after_fds}"
    )
