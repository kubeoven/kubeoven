from kubeoven import pki, state, ssh
from .create_ctrl_mgr_manifest import create_ctrl_mgr_manifest
from .create_ctrl_mgr_certs import create_ctrl_mgr_certs
from .create_ctrl_mgr_kubeconf import create_ctrl_mgr_kubeconf


def deploy_ctrl_manager(
    full_state: state.FullState, address: str, ca: pki.KeyPair, client: ssh.NodeClient
):
    current, next = full_state.get_node_states(address)
    if current.kube_controller_manager.should_deploy(next.kube_controller_manager):
        deploy_new_ctrl_manager(full_state, ca, client)
    if current.kube_controller_manager != next.kube_controller_manager:
        current.kube_controller_manager = next.kube_controller_manager
        full_state.current.commit()
        return True
    return False


def deploy_new_ctrl_manager(
    full_state: state.FullState, ca: pki.KeyPair, client: ssh.NodeClient
):
    create_ctrl_mgr_manifest(full_state.config, client)
    cert = create_ctrl_mgr_certs(ca)
    create_ctrl_mgr_kubeconf(ca, cert, client)
