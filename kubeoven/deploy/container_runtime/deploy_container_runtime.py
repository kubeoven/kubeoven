from kubeoven import log
from kubeoven.state import FullState
from kubeoven.ssh import NodeClient
from .upload_containerd import upload_containerd
from .upload_runc import upload_runc
from .create_containerd_conf import create_containerd_conf
from .create_containerd_service import create_containerd_service

def deploy_container_runtime(full_state:FullState, address: str, client: NodeClient):
    current, next = full_state.get_node_states(address)
    if current.containerd.should_deploy(next.containerd):
        deploy_new_container_runtime(full_state, client)
    if current.containerd != next.containerd:
        current.containerd = next.containerd
        full_state.current.commit()
        return True
    return False


def deploy_new_container_runtime(full: FullState, client: NodeClient):
    log.info('deploy containerd')
    client.stop_service('containerd')
    upload_runc(full.config, client)
    upload_containerd(full.config, client)
    create_containerd_conf(client, full.config.registry_node() or "")
    create_containerd_service(client)
    client.start_service('containerd', restart=False)
