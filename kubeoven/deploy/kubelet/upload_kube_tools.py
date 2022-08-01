import os
from kubeoven import binary, conf, ssh, templates
from kubeoven.common import to_amd

def upload_kube_tools(cluster: conf.ClusterConf, client: ssh.NodeClient):
    upload_cni_plugins(cluster, client)
    upload_crictl(cluster, client)
    upload_kubelet(cluster, client)
    upload_kubectl(cluster, client)

def upload_cni_plugins(cluster: conf.ClusterConf,client: ssh.NodeClient):
    bin = binary.get_binary("cni-plugins", cluster.cni_plugins_version, client.os, to_amd(client.arch))
    dest = os.path.join('/tmp', bin.filename)
    binary.copy_binary_to_node(bin, dest, cluster.cache_server, client)
    client.ensure_dirs('/opt/cni/bin')
    client.exec_command(f"sudo tar -zxvf {dest} --directory /opt/cni/bin")

def upload_crictl(cluster: conf.ClusterConf, client: ssh.NodeClient):
    bin = binary.get_binary('crictl', cluster.kubernetes_version, client.os, to_amd(client.arch))
    dest = os.path.join('/tmp', bin.filename)
    binary.copy_binary_to_node(bin, dest, cluster.cache_server, client)
    client.exec_command(f"sudo tar -zxvf {dest} --directory /usr/local/bin")
    data = templates.render('crictl.yaml.j2')
    client.write_file('/etc/crictl.yaml', data)

def upload_kubelet(cluster: conf.ClusterConf, client: ssh.NodeClient):
    bin = binary.get_binary('kubelet', cluster.kubernetes_version, client.os, to_amd(client.arch))
    dest = os.path.join('/usr/local/bin', bin.filename)
    binary.copy_binary_to_node(bin, dest, cluster.cache_server, client)
    client.exec_command(f'sudo chmod +x {dest}')


def upload_kubectl(cluster: conf.ClusterConf, client:ssh.NodeClient):
    bin = binary.get_binary('kubectl', cluster.kubernetes_version, client.os, to_amd(client.arch))
    dest = os.path.join('/usr/local/bin', bin.filename)
    binary.copy_binary_to_node(bin, dest, cluster.cache_server, client)
    client.exec_command(f'sudo chmod +x {dest}')

    