import os
from kubeoven import ssh, conf, binary
from kubeoven.common import to_amd

def upload_runc(cluster: conf.ClusterConf, client: ssh.NodeClient):
    bin = binary.get_binary("runc", cluster.runc_version, client.os, to_amd(client.arch))
    dst = '/usr/local/bin/runc'
    binary.copy_binary_to_node(bin, dst, cluster.cache_server, client)
    client.exec_command(f"sudo chmod +x {dst}")
