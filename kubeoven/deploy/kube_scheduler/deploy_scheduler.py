from kubeoven.pki import KeyPair
from kubeoven.ssh import NodeClient
from kubeoven.state import FullState
from .create_scheduler_manifest import create_scheduler_manifest
from .create_scheduler_certs import create_scheduler_certs
from .create_scheduler_kubeconf import create_scheduler_kubeconf

def deploy_scheduler(full_state: FullState, address: str, ca: KeyPair, sftp: NodeClient):
    current, next = full_state.get_node_states(address)
    if current.kube_scheduler.should_deploy(next.kube_scheduler):
        create_scheduler_manifest(full_state.config, sftp)
        cert = create_scheduler_certs(ca)
        create_scheduler_kubeconf(ca, cert, sftp)
    if current.kube_scheduler != next.kube_scheduler:
        current.kube_scheduler = next.kube_scheduler
        full_state.current.commit()
        return True
    return False
