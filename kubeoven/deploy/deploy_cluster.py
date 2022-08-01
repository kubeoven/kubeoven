from kubeoven import pki
from kubeoven.state import FullState, get_kube_ca
from .deploy_controlplane import deploy_controlplane
from .deploy_wokerplane import deploy_workerplane
from .deploy_cache import deploy_cache
from .deploy_etcd_cluster import deploy_etcd_cluster
from .deploy_manifests import deploy_manifests
from .deploy_registry import deploy_registry

def deploy_cluster(full_state: FullState):
    kube_ca = get_kube_ca(full_state)
    deploy_cache(full_state, kube_ca)
    deploy_registry(full_state, kube_ca)
    deploy_etcd_cluster(full_state, kube_ca)
    deploy_controlplane(full_state, kube_ca)
    deploy_workerplane(full_state, kube_ca)
    deploy_manifests(full_state)
