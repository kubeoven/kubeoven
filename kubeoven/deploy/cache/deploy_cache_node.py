from kubeoven import ssh, log
from kubeoven.state import FullState
from .create_cache_service import create_cache_service
from .download_caddy import download_caddy
from .upload_cache import upload_cache


def deploy_cache_node(full_state: FullState, address: str):
    current, next = full_state.get_node_states(address)
    if current.cache_server.should_deploy(next.cache_server):
        deploy_new_cache_node(full_state, address)
    if current.cache_server != next.cache_server:
        current.cache_server = next.cache_server
        full_state.current.commit()

def deploy_new_cache_node(full_state: FullState, address:str):
    log.info("deploy cache")
    with ssh.create_node_client(full_state, address) as client:
        download_caddy(client)
        client.ensure_dirs("/var/cache/kubeoven")
        upload_cache(full_state, address)
        create_cache_service(client)
        client.start_service("kubeoven-cache")
