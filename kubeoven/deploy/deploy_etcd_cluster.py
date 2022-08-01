from kubeoven import log
from kubeoven.pki import KeyPair
from kubeoven.state import FullState
from .etcd import deploy_etcd_node


def deploy_etcd_cluster(full_state: FullState, ca: KeyPair):
    for address in full_state.resources_keys():
        node, _ = full_state.get_node_conf(address)
        if 'etcd' not in node.role:
            continue
        log.set_hostname(node.hostname)
        deploy_etcd_node(full_state, address, ca)
 
