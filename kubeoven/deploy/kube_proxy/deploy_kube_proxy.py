from kubeoven.state import FullState
from kubeoven.ssh import NodeClient
from .create_kube_proxy_manifest import create_kube_proxy_manifest

def deploy_kube_proxy(full_state: FullState, client: NodeClient):
    current, next = full_state.get_addons_states()
    if current.kube_proxy.should_deploy(next.kube_proxy):
        deploy_new_kube_proxy(full_state, client)
    if current.kube_proxy != next.kube_proxy:
        current.kube_proxy = next.kube_proxy
        full_state.current.commit()
        return True
    return False
    
def deploy_new_kube_proxy(full: FullState, client: NodeClient):
    create_kube_proxy_manifest(full, client)

