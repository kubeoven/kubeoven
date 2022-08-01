from paramiko import SFTPClient
from kubeoven import pki, log, ssh
from kubeoven.conf import NodeConf
from kubeoven.pki import KeyPair, pem_encode_cert, pem_encode_key


def create_apiserver_certs(ca: pki.KeyPair, node: NodeConf, client: ssh.NodeClient):
    dst = pki.base_dir
    apiserver = create_apiserver_cert(ca, node)
    kubelet = create_apiserver_kubelet_cert(ca)
    account = create_service_account_cert(ca)
    etcd = create_apiserver_etcd_cert(ca)
    client.write_file(f"{dst}/apiserver.crt", pem_encode_cert(apiserver.cert))
    client.write_file(f"{dst}/apiserver.key", pem_encode_key(apiserver.key))
    client.write_file(f"{dst}/apiserver-kubelet-client.crt", pem_encode_cert(kubelet.cert))
    client.write_file(f"{dst}/apiserver-kubelet-client.key", pem_encode_key(kubelet.key))
    client.write_file(f"{dst}/apiserver-etcd-client.crt", pem_encode_cert(etcd.cert))
    client.write_file(f"{dst}/apiserver-etcd-client.key", pem_encode_key(etcd.key))
    client.write_file(f"{dst}/sa.crt", pem_encode_cert(account.cert))
    client.write_file(f"{dst}/sa.key", pem_encode_key(account.key))

def create_apiserver_cert(ca: pki.KeyPair, node: NodeConf):
    log.info("create kube-apiserver certs")
    dns = [
        "kubernetes",
        "kubernetes.default",
        "kubernetes.default.svc",
        "kubernetes.default.svc.cluster.local",
        node.hostname
    ]
    addresses = [node.address, "10.96.0.1", "127.0.0.1"]
    return pki.create_cert(
        ca=ca,
        cn="kube-apiserver",
        org="",
        addresses=addresses,
        dns=dns,
        key_usage=pki.KeyUsageServer,
    )

def create_apiserver_kubelet_cert(ca:KeyPair):
    return pki.create_cert(
        ca=ca,
        cn="kube-apiserver-kubelet-client",
        org="system:masters",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageClient,
    )

def create_service_account_cert(ca:KeyPair):
    log.info("create service account certs")
    return pki.create_cert(
        ca=ca,
        cn="service-accounts",
        org="",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageBoth,
    )

def create_apiserver_etcd_cert(ca: pki.KeyPair):
    return pki.create_cert(
        ca=ca,
        cn="kube-apiserver-etcd-client",
        org="system:masters",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageClient,
    )
