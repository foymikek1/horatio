#!/usr/bin/env python3
import sys
from pathlib import Path

# Ensure that our project root is on sys.path, even when launched via subprocess
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import threading
import subprocess
import time

import paramiko

from ssh_server.config import load_config
from ssh_server.hostkey import load_host_key
from ssh_server.network import create_socket

def start_server():
    cfg = load_config()
    host_key = load_host_key("ssh_server/ssh_host_rsa_key")
    sock = create_socket(cfg["port"])
    print(f"[server] Listening on 127.0.0.1:{cfg['port']}")

    while True:
        client_sock, _ = sock.accept()
        transport = paramiko.Transport(client_sock)
        transport.add_server_key(host_key)

        # simple ServerInterface for username/password + session channels only
        class _S(paramiko.ServerInterface):
            def check_auth_password(self, u, p):
                return paramiko.AUTH_SUCCESSFUL if (u == cfg["username"] and p == cfg["password"]) else paramiko.AUTH_FAILED

            def get_allowed_auths(self, u):
                return "password"

            def check_channel_request(self, kind, cid):
                return paramiko.OPEN_SUCCEEDED if kind == "session" else paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

        transport.start_server(server=_S())

        chan = transport.accept(cfg["idle_timeout"])
        if chan is None:
            transport.close()
            continue

        # once we have a session, run the VM subprocess and forward its stdout
        prog = sys.argv[1] if len(sys.argv) > 1 else None
        if not prog:
            chan.send(b"Error: no program specified.\n")
            chan.close()
            continue

        proc = subprocess.Popen(
            [str(sys.executable), "vm_core/src/vm", prog],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        def _forward():
            for line in proc.stdout:
                chan.send(line.encode())
            proc.wait()
            chan.close()
            transport.close()

        threading.Thread(target=_forward, daemon=True).start()

if __name__ == "__main__":
    start_server()
