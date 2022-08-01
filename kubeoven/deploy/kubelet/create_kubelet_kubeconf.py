import base64
from kubeoven import pki, ssh, log, templates
from kubeoven.conf import NodeConf
from kubeoven.pki import KeyPair

def create_kubelet_kubeconf(node: NodeConf, ca: KeyPair, cert: KeyPair, client:ssh.NodeClient):
    dst = '/etc/kubernetes/kubelet.conf'
    log.info(f'write {dst}')
    user = f"system:node:{node.hostname}"
    data = templates.render(
        "kubeconfig.yaml.j2",
        user=user,
        ca_cert=base64.b64encode(pki.pem_encode_cert(ca.cert)).decode(),
        cert=base64.b64encode(pki.pem_encode_cert(cert.cert)).decode(),
        cert_key=base64.b64encode(pki.pem_encode_key(cert.key)).decode(),
    )
    client.write_file(dst, data)
