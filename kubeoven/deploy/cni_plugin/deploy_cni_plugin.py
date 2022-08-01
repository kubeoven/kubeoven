from kubeoven.state import FullState, full_state
from kubeoven.ssh import NodeClient
from .deploy_flannel import deploy_flannel

def deploy_cni_plugin(full_state: FullState, client: NodeClient):
    current, next = full_state.get_addons_states()
    if current.cni_plugin.should_deploy(next.cni_plugin):
        deploy_new_cni_plugin(full_state, client)
    if current.cni_plugin != next.cni_plugin:
        current.cni_plugin = next.cni_plugin
        full_state.current.commit()
        return True
    return False
    
def deploy_new_cni_plugin(full: FullState, client: NodeClient):
    if full.config.network.plugin == 'flannel':
        return deploy_flannel

