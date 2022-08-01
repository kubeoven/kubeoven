import os
from kubeoven import conf, ssh, binary
from kubeoven.common import to_amd

def upload_registry(cluster: conf.ClusterConf, client: ssh.NodeClient):
    bin = binary.get_binary("registry", cluster.registry_version, client.os, to_amd(client.arch))
    dst = os.path.join('/tmp', bin.filename)
    binary.copy_binary_to_node(bin, dst, cluster.cache_server, client)
    cmd = f"tar -zxvf {dst} --directory=/usr/local/bin --wildcards 'registry'"
    client.exec_command(f"sudo {cmd}")


