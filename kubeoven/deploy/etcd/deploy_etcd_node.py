from kubeoven import log, ssh
from kubeoven.pki import KeyPair
from kubeoven.state import FullState
from .get_initial_cluster import get_initial_cluster
from .create_etcd_service import create_etcd_service
from .clean_etcd_data_dir import clean_etcd_data_dir
from .add_etcd_member import add_etcd_member
from .upload_etcd import upload_etcd
from .create_etcd_certs import create_etcd_certs


def deploy_etcd_node(full: FullState, address: str, ca: KeyPair):
    current, next = full.get_node_states(address)
    if current.etcd.should_deploy(next.etcd):
        deploy_new_etcd_node(full, address, ca)
    elif current.etcd.should_undeploy(next.etcd):
        undeploy_etcd_node(full, address, ca)
    if current.etcd != next.etcd:
        current.etcd = next.etcd
        full.current.commit()


def deploy_new_etcd_node(full_state: FullState, address: str, ca: KeyPair):
    with ssh.create_node_client(full_state, address) as client:
        log.info("deploy etcd")
        node, _ = full_state.get_node_conf(address)
        client.stop_service('etcd')
        clean_etcd_data_dir(client)
        upload_etcd(full_state.config, client)
        initial_cluster = get_initial_cluster(full_state)
        create_etcd_certs(ca, node, client)
        if len(initial_cluster) > 0:
            add_etcd_member(full_state, node, client)
        create_etcd_service(node, initial_cluster, client)
        client.start_service("etcd", True)

def undeploy_etcd_node(full_state: FullState, address: str, ca: KeyPair):
    pass
    