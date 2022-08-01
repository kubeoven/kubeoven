from kubeoven import ssh
from kubeoven.state import FullState, get_present_controlplane_nodes
from .create_nginx_config import create_nginx_config
from .create_nginx_manifest import create_nginx_manifest


def deploy_nginx_proxy(full_state: FullState, address: str, client: ssh.NodeClient):
    current, next = full_state.get_node_states(address)
    if current.nginx_proxy.should_deploy(next.nginx_proxy):
        deploy_new_nginx_proxy(full_state, client)
    if current.nginx_proxy != next.nginx_proxy:
        current.nginx_proxy = next.nginx_proxy
        full_state.current.commit()
        return True
    return False


def deploy_new_nginx_proxy(full_state: FullState, client: ssh.NodeClient):
    addresses = get_present_controlplane_nodes(full_state)
    client.ensure_dirs('/etc/kubernetes/nginx-proxy')
    hash = create_nginx_config(addresses, client)
    create_nginx_manifest(hash, client)

