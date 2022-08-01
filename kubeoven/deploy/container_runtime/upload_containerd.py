import os
from kubeoven import ssh, conf, binary, common

def upload_containerd(cluster: conf.ClusterConf, client: ssh.NodeClient):
    bin = binary.get_binary("containerd", cluster.containerd_version, client.os, common.to_amd(client.arch))
    dst = os.path.join('/tmp', bin.filename)
    binary.copy_binary_to_node(bin, dst, cluster.cache_server, client)
    cmd = f"tar -zxvf {dst} --directory=/usr/local/bin --strip-components=1"
    client.exec_command(f"sudo {cmd}")
