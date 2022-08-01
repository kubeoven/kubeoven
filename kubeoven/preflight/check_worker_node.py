from kubeoven import ssh
from kubeoven.exceptions import AppException
from .check_kernel_mods import check_kernel_mods
from .check_networking import check_networking

def check_worker_node(client: ssh.NodeClient):
    check_kernel_mods(client)
    check_networking(client)
    port = 10250
    if client.is_port_open(port):
        raise AppException(f"port {port} is in use", hostname=client.hostname)
