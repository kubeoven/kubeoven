from kubeoven import log
from kubeoven.pki import KeyPair
from kubeoven.conf import NodeConf, ClusterConf
from kubeoven.state import FullState
from kubeoven.ssh import NodeClient
from .create_kubelet_config import create_kubelet_config
from .create_kubelet_kubeconf import create_kubelet_kubeconf
from .create_kubelet_service import create_kubelet_service
from .create_admin_kubeconf import create_admin_kubeconf
from .create_kubelet_certs import create_kubelet_certs
from .ensure_node_dirs import ensure_node_dirs
from .upload_kube_tools import upload_kube_tools
from .create_kube_proxy_conf import create_kube_proxy_conf


def deploy_kubelet(full_state:FullState, address: str, ca: KeyPair, client: NodeClient):
    node, _ = full_state.get_node_conf(address)
    current, next = full_state.get_node_states(address)
    if current.kubelet.should_deploy(next.kubelet):
        ensure_node_dirs(client)
        upload_kube_tools(full_state.config, client)
        deploy_new_kubelet(full_state.config, node, ca, client)
    if current.kubelet != next.kubelet:
        current.kubelet = next.kubelet
        full_state.current.commit()
        return True
    return False
        

def deploy_new_kubelet(cluster: ClusterConf, node: NodeConf, ca: KeyPair, client: NodeClient):
    log.info('deploy kublet')
    client.stop_service('kubelet')
    cert = create_kubelet_certs(node, ca, client)
    create_kubelet_config(client)
    create_kubelet_kubeconf(node, ca, cert, client)
    # create_kube_proxy_conf(cluster, node, ca, client)
    create_kubelet_service(client, node)
    create_admin_kubeconf(ca, client)
