from kubeoven import ssh
from kubeoven.state import FullState, get_present_controlplane_node
from .kube_proxy import deploy_kube_proxy


def deploy_addons(full_state:FullState):
    address = get_present_controlplane_node(full_state)
    with ssh.create_node_client(full_state, address) as client:
        deploy_kube_proxy(full_state, client)
