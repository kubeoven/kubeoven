from kubeoven import ssh
from kubeoven.exceptions import AppException

def check_etcd_node(client: ssh.NodeClient):
    for port in [2379, 2380]:
        if client.is_port_open(port):
            msg = f"port {port} is in use"
            raise AppException(msg, hostname=client.hostname)
