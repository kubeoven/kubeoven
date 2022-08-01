from kubeoven.conf import NodeConf
from kubeoven.ssh import NodeClient
from kubeoven.state import FullState
from kubeoven import state, log


def add_etcd_member(full_state: FullState, node: NodeConf, client: NodeClient):
    log.info('add etcd member')
    addresses = state.get_present_etcd_nodes(full_state)
    if len(addresses) == 0:
        raise RuntimeError("no existing etcd nodes are present")
    endpoints = [f'{address}:2379' for address in addresses]
    cmd = [
        "etcdctl member add",
        node.hostname,
        f"--peer-urls=https://{node.address}:2380",
        f"--endpoints={','.join(endpoints)}",
        "--cacert=/etc/kubernetes/pki/ca.crt",
        "--cert=/etc/kubernetes/pki/etcd/client.crt",
        "--key=/etc/kubernetes/pki/etcd/client.key",
    ]
    client.exec_command(" ".join(cmd))
