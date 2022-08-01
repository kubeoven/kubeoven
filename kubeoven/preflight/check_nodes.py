from typing import List
from kubeoven import ssh
from kubeoven.state import FullState
from multiprocessing import Pool, cpu_count
from .check_controlplane_node import check_controlplane_node
from .check_worker_node import check_worker_node
from .check_etcd_node import check_etcd_node
from .check_required_cmds import check_required_cmds


def check_nodes(full_state: FullState):
    nodes = []
    for addr in full_state.resources_keys():
        roles = []
        current, next = full_state.get_node_states(addr)
        if current.etcd.should_deploy(next.etcd):
            roles.append('etcd')
        if current.kubelet.should_deploy(next.kubelet):
            roles.append('worker')
        if current.kube_apiserver.should_deploy(next.kube_apiserver):
            roles.append('controlplane')
        if len(roles) > 0:
            nodes.append([full_state, addr, roles])
    if len(nodes):
        with Pool(processes=1) as pool:
            pool.starmap(check_node, nodes)

def check_node(full_state: FullState, address: str, roles: List[str]):
    with ssh.create_node_client(full_state, address) as client:
        check_required_cmds(client)
        if 'etcd' in roles:
            check_etcd_node(client)
        if 'worker' in roles:
            check_worker_node(client)
        if 'controlplane' in roles:
            check_controlplane_node(client)
