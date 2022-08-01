from kubeoven import ssh
from kubeoven.state import FullState
from .upload_registry import upload_registry
from .create_registry_config import create_registry_config
from .create_registry_service import create_registry_service
from .download_images import download_images, ensure_crane_cli
from .upload_images import upload_images


def deploy_registry_node(full_state: FullState, address: str):
    current, next = full_state.get_node_states(address)
    if current.registry.should_deploy(next.registry):
        deploy_new_registry_node(full_state, address)
    if current.registry != next.registry:
        current.registry = next.registry
        # full_state.current.commit()


def deploy_new_registry_node(full_state: FullState, address: str):
    with ssh.create_node_client(full_state, address) as client:
        upload_registry(full_state.config, client)
        create_registry_config(client)
        create_registry_service(client)
        client.start_service('registry')
        ensure_crane_cli(full_state.config)
        download_images(full_state)
        upload_images(full_state)

