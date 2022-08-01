from kubeoven import conf
from .node_state import NodeState
from .process_state import Status
from .process_state import ProcessState


def build_node_state(node: conf.NodeConf, cluster: conf.ClusterConf) -> NodeState:
    k8s_version = cluster.kubernetes_version
    state = NodeState(config=node)
    if "registry" in node.role:
        state.registry = ProcessState(status=Status.PRESENT, version=cluster.registry_version)
    if "cache" in node.role:
        state.cache_server = ProcessState(status=Status.PRESENT, version="v2.4.6")
    if "etcd" in node.role:
        state.etcd = ProcessState(status=Status.PRESENT, version=cluster.etcd_version)
    if "worker" in node.role:
        state.containerd = ProcessState(
            status=Status.PRESENT, version=cluster.containerd_version
        )
        state.kubelet = ProcessState(status=Status.PRESENT, version=k8s_version)
        state.nginx_proxy = ProcessState(
            status=Status.PRESENT,
            version="1.21",
            depends=set(cluster.controlplane_nodes),
        )
    if "controlplane" in node.role:
        state.containerd = ProcessState(
            status=Status.PRESENT, version=cluster.containerd_version
        )
        state.kubelet = ProcessState(status=Status.PRESENT, version=k8s_version)
        state.kube_apiserver = ProcessState(
            status=Status.PRESENT, version=k8s_version, depends=set(cluster.etcd_nodes)
        )
        state.kube_controller_manager = ProcessState(
            status=Status.PRESENT, version=k8s_version
        )
        state.kube_scheduler = ProcessState(status=Status.PRESENT, version=k8s_version)
        state.nginx_proxy = ProcessState(status=Status.ABSENT, version="")
    return state