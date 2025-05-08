import os
from typing import Dict

# Default settings
DEFAULT_USER = "lab"
DEFAULT_PASS = "lab"
DEFAULT_PORT = 2222
DEFAULT_IDLE_TIMEOUT = 5.0

def load_config() -> Dict[str, object]:
    """
    Load SSH server settings from environment variables, with fallbacks.
    Returns a dict:
      {
        "username": str,
        "password": str,
        "port": int,
        "idle_timeout": float,
      }
    """
    username = os.getenv("SSH_USER", DEFAULT_USER)
    password = os.getenv("SSH_PASS", DEFAULT_PASS)

    port_str = os.getenv("SSH_PORT", "")
    try:
        port = int(port_str) if port_str else DEFAULT_PORT
    except ValueError:
        raise ValueError(f"Invalid SSH_PORT value: {port_str!r}")

    idle_str = os.getenv("SSH_IDLE_TIMEOUT", "")
    try:
        idle_timeout = float(idle_str) if idle_str else DEFAULT_IDLE_TIMEOUT
    except ValueError:
        raise ValueError(f"Invalid SSH_IDLE_TIMEOUT value: {idle_str!r}")

    return {
        "username": username,
        "password": password,
        "port": port,
        "idle_timeout": idle_timeout,
    }
