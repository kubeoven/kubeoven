from kubeoven import log, ssh
from kubeoven.pki import KeyPair
from kubeoven.conf import NodeConf
from kubeoven.state import FullState
from kubeoven.health import health_check_control_node
from .kubelet import deploy_kubelet, start_kubelet
from .kube_apiserver import deploy_apiserver
from .kube_controller_manager import deploy_ctrl_manager
from .kube_scheduler import deploy_scheduler
from .container_runtime import deploy_container_runtime
import backoff

def deploy_controlplane(full_state: FullState, ca: KeyPair):
    for address in full_state.resources_keys():
        node, _ = full_state.get_node_conf(address)
        has_changes = full_state.has_controlplane_changes(address)
        if 'controlplane' in node.role and has_changes:
            deploy_controlplane_node(full_state, node, ca)

def deploy_controlplane_node(full_state: FullState, node: NodeConf, ca: KeyPair):
    with ssh.create_node_client(full_state, node.address) as client:
        log.set_hostname(node.hostname)
        deployments = [
            deploy_container_runtime(full_state, node.address, client),
            deploy_kubelet(full_state, node.address, ca, client),
            deploy_apiserver(full_state, node.address, ca, client),
            deploy_ctrl_manager(full_state, node.address, ca, client),
            deploy_scheduler(full_state, node.address, ca, client),
        ]
        if any(deployments):
            start_kubelet(client)
            health_check_control_node(node, client.ssh)
            set_master_node_labels(node, client)

@backoff.on_exception(backoff.expo, Exception, max_tries=8)
def set_master_node_labels(node: NodeConf, client: ssh.NodeClient):
    label = 'node-role.kubernetes.io/master=""'
    config = '--kubeconfig /etc/kubernetes/admin.conf'
    cmd = f'kubectl label node {node.hostname} {label} {config}'
    client.exec_command(cmd)
