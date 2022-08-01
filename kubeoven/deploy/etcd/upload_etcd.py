import os
from kubeoven import binary, ssh, conf
from kubeoven.common import to_amd

def upload_etcd(cluster: conf.ClusterConf, client: ssh.NodeClient):
    bin = binary.get_binary("etcd", cluster.etcd_version, client.os, to_amd(client.arch))
    dst = os.path.join('/tmp', bin.filename)
    binary.copy_binary_to_node(bin, dst, cluster.cache_server, client)
    sub_dir = bin.filename.replace('.tar.gz', '')
    cmd = f"tar -zxvf {dst} --directory=/usr/local/bin --strip-components=1  --wildcards '{sub_dir}/etcd*'"
    client.exec_command(f"sudo {cmd}")
