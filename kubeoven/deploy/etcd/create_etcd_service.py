from typing import List
from kubeoven import ssh, log, templates
from kubeoven.conf import NodeConf
from .etcd_common import etcd_peer_url


def create_etcd_service(node: NodeConf, initial_cluster: List[str], client: ssh.NodeClient):
    dst = '/etc/systemd/system/etcd.service'
    initial_cluster.append(f"{node.hostname}={etcd_peer_url(node.address)}")
    initial_cluster_state = "existing" if len(initial_cluster) > 1 else "new"
    log.info(f"etcd cluster state {initial_cluster_state}")
    log.info(f'write {dst}')
    data = templates.render(
        "etcd.service.j2",
        hostname=node.hostname,
        address=node.address,
        initial_cluster=",".join(initial_cluster),
        initial_cluster_state=initial_cluster_state,
    )
    client.write_file(dst, data)
    client.exec_command('sudo systemctl daemon-reload')
