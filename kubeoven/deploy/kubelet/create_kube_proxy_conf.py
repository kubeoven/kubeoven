from kubeoven import log, templates, ssh, pki
from kubeoven.conf import NodeConf, ClusterConf
from kubeoven.ssh import NodeClient
from kubeoven.pki import KeyPair
import base64

def create_kube_proxy_conf(cluster: ClusterConf, node: NodeConf, ca: KeyPair, client: NodeClient):
    cert = create_kube_proxy_certs(ca)
    create_kube_proxy_kubeconf(node, ca, cert, client)
    data = templates.render("kube_proxy_config.yaml.j2", cluster_cidr=cluster.cluster_cidr)
    dst = '/var/lib/kube-proxy/kube-proxy-config.yaml'
    client.write_file(dst, data)


def create_kube_proxy_certs(ca: KeyPair):
    log.info("create kube-proxy certs")
    return pki.create_cert(
        ca=ca,
        cn="system:kube-proxy",
        org="",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageBoth,
    )


def create_kube_proxy_kubeconf(node: NodeConf, ca: KeyPair, cert: KeyPair, client: ssh.NodeClient):
    dst = "/var/lib/kube-proxy/kubeconfig.conf"
    log.info(f"write {dst}")
    data = templates.render(
        "kubeconfig.yaml.j2",
        user="system:kube-proxy",
        server=node.address,
        ca_cert=base64.b64encode(pki.pem_encode_cert(ca.cert)).decode(),
        cert=base64.b64encode(pki.pem_encode_cert(cert.cert)).decode(),
        cert_key=base64.b64encode(pki.pem_encode_key(cert.key)).decode(),
    )
    client.write_file(dst, data)
