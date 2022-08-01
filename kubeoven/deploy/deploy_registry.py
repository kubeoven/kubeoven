from kubeoven.pki import KeyPair
from kubeoven.state import FullState
from .registry import deploy_registry_node

def deploy_registry(full_state: FullState, _: KeyPair):
    for address in full_state.resources_keys():
        node, _ = full_state.get_node_conf(address)
        if 'registry' in node.role:
            deploy_registry_node(full_state, node.address)
