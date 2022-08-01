from kubeoven import ssh, log
from kubeoven.pki import KeyPair
from kubeoven.conf import NodeConf
from kubeoven.state import FullState
from kubeoven.health import health_check_worker_node
from .kubelet import deploy_kubelet, start_kubelet
from .nginx_proxy import deploy_nginx_proxy
from .container_runtime import deploy_container_runtime
import backoff


def deploy_workerplane(full: FullState, ca: KeyPair):
    for address in full.resources_keys():
        node, _ = full.get_node_conf(address)
        if 'worker' in node.role and full.has_workerplane_changes(address):
            deploy_worker_node(full, node, ca)

def deploy_worker_node(full_state: FullState, node: NodeConf, ca: KeyPair):
    log.set_hostname(node.hostname)
    with ssh.create_node_client(full_state, node.address) as client:
        deployments = [
            deploy_container_runtime(full_state, node.address, client),
            deploy_kubelet(full_state, node.address, ca, client),
            deploy_nginx_proxy(full_state, node.address, client)
        ]
        if any(deployments):
            start_kubelet(client)
            health_check_worker_node(node, client.ssh)
            set_worker_node_labels(node, client)

@backoff.on_exception(backoff.expo, Exception, max_tries=8)
def set_worker_node_labels(node: NodeConf, client: ssh.NodeClient):
    label = 'node-role.kubernetes.io/worker=""'
    config = '--kubeconfig /etc/kubernetes/admin.conf'
    cmd = f'kubectl label node {node.hostname} {label} {config}'
    client.exec_command(cmd)

