from kubeoven import ssh
from paramiko import SSHClient
from .health_check_request import health_check_request


def health_check_nginx_proxy(client: SSHClient):
    with ssh.forward("localhost", 6443, client) as f:
        server, port = f.server_address
        url = f'https://{server}:{port}/healthz'
        health_check_request(url, 'nginx-proxy')
