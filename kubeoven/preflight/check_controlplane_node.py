from kubeoven import ssh
from kubeoven.exceptions import AppException
from .check_kernel_mods import check_kernel_mods
from .check_networking import check_networking

def check_controlplane_node(client: ssh.NodeClient):
    check_kernel_mods(client)
    check_networking(client)
    for port in [6443, 10250, 10259, 10257]:
        if client.is_port_open(port):
            msg = f"port {port} is in use"
            raise AppException(msg, hostname=client.hostname)
