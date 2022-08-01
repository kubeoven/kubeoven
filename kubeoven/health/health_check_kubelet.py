from kubeoven import ssh
from paramiko import SSHClient
from .health_check_request import health_check_request


def health_check_kubelet(client: SSHClient):
    with ssh.forward("localhost", 10248, client) as f:
        server, port = f.server_address
        url = f'http://{server}:{port}/healthz'
        health_check_request(url, 'kubelet')
        