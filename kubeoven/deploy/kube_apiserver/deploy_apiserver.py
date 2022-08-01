from kubeoven import ssh, log, templates
from kubeoven.conf import ClusterConf, NodeConf
from kubeoven.pki import KeyPair
from kubeoven.state import FullState
from kubeoven.constants import K8S_GCR_REGISTRY
from .create_apiserver_certs import create_apiserver_certs

def deploy_apiserver(full_state:FullState, address: str, ca: KeyPair, client: ssh.NodeClient):
    node, _ = full_state.get_node_conf(address)
    current, next = full_state.get_node_states(address)
    if current.kube_apiserver.should_deploy(next.kube_apiserver):
        deploy_new_apiserver(full_state.config, node, ca, client)
    if current.kube_apiserver != next.kube_apiserver:
        current.kube_apiserver = next.kube_apiserver
        full_state.current.commit()
        return True
    return False
        

def deploy_new_apiserver(cluster: ClusterConf, node: NodeConf, ca: KeyPair, client: ssh.NodeClient):
    create_apiserver_certs(ca, node, client)
    dst = '/etc/kubernetes/manifests/kube-apiserver.yaml'
    log.info(f'write {dst}')
    data = templates.render(
        "kube_apiserver.yaml.j2",
        address=node.address,
        version=cluster.kubernetes_version,
        etcd_servers=','.join(cluster.etcd_servers),
        registry=cluster.registry_uri(default=K8S_GCR_REGISTRY)
    )
    client.write_file(dst, data)
