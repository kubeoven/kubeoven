
from kubeoven import ssh, log


def start_kubelet(client: ssh.NodeClient):
    log.info('start kubelet service')
    client.exec_command("sudo systemctl restart kubelet.service")
    client.exec_command("sudo systemctl enable kubelet.service")
    