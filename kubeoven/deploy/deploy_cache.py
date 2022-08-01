from kubeoven.pki import KeyPair
from kubeoven.state import FullState
from .cache import deploy_cache_node

def deploy_cache(full_state: FullState, _: KeyPair):
    for address in full_state.resources_keys():
        node, __ = full_state.get_node_conf(address)
        if 'cache' in node.role:
            deploy_cache_node(full_state, node.address)
