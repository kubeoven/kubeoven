from kubeoven import conf, log
from .full_state import ClusterState
from .build_node_state import build_node_state
from .build_manifests import build_cluster_manifests

def build_next_state(cluster: conf.ClusterConf):
    log.info("building next state")
    state = ClusterState()
    for node in cluster.nodes:
        state.resources[node.address] = build_node_state(node, cluster)
    state.manifests = build_cluster_manifests(cluster)
    return state




