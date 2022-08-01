from kubeoven import log, pki, ssh
from kubeoven.conf import NodeConf
from kubeoven.pki import KeyPair, create_cert


def create_kubelet_certs(node:NodeConf, ca: KeyPair, client: ssh.NodeClient) -> KeyPair:
    log.info("create kubelet certs")
    cert = create_cert(
        ca=ca,
        cn=f"system:node:{node.hostname}",
        org="system:nodes",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageBoth,
    )
    write_kubelet_certs(ca, cert, client)
    return cert
    
def write_kubelet_certs(ca: KeyPair, cert: KeyPair, client: ssh.NodeClient):
    dst = pki.base_dir
    client.write_file(f"{dst}/ca.crt", pki.pem_encode_cert(ca.cert))
    client.write_file(f"{dst}/ca.key", pki.pem_encode_key(ca.key))
    client.write_file(f"{dst}/kubelet.crt", pki.pem_encode_cert(cert.cert))
    client.write_file(f"{dst}/kubelet.key", pki.pem_encode_key(cert.key))
