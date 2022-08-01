from kubeoven import ssh


def ensure_node_dirs(client:ssh.NodeClient):
    pass
    # client.ensure_dirs(
    #     '/opt/cni/bin',
    #     '/var/lib/etcd',
    #     '/var/lib/kubelet',
    #     '/var/lib/kube-proxy',
    #     '/etc/kubernetes',
    #     '/etc/kubernetes/pki',
    #     '/etc/kubernetes/pki/etcd',
    #     '/etc/kubernetes/manifests')