import paramiko


def load_host_key(path: str) -> paramiko.RSAKey:
    return paramiko.RSAKey(filename=path)
