# ssh_server/core.py
# is the heart of the SSH-VM bridge.
#Tests launch your thin wrapper ssh_server/server.py, 
# which calls start_server(cfg) here.

import threading
import paramiko
from .config import ServerConfig
from .hostkey import load_host_key
from .network import handle_ssh_channel

def start_server(cfg: ServerConfig):
    # Load the RSA host key for this server
    host_key = load_host_key(cfg.host_key_path)

    # Bind and listen on 0.0.0.0:cfg.port
    transport = paramiko.Transport(("0.0.0.0", cfg.port))
    transport.add_server_key(host_key)

    # Build Paramiko “server” subclass from your config
    server = ServerConfig.to_paramiko_server(cfg)
    transport.start_server(server=server)

    # Accept connections forever…
    while True:
        chan = transport.accept(timeout=30)
        if chan is None:
            continue

        # When a client connects, hand it off to your channel handler
        t = threading.Thread(target=handle_ssh_channel, args=(chan, cfg))
        t.daemon = True
        t.start()
