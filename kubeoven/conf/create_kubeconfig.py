from base64 import b64encode
from kubeoven import pki, templates

def create_kubeconfig(ca: pki.KeyPair, cert: pki.KeyPair, user: str):
    return templates.render(
        "kubeconfig.yaml.j2",
        user=user,
        ca_cert=b64encode(pki.pem_encode_cert(ca.cert)).decode(),
        cert=b64encode(pki.pem_encode_cert(cert.cert)).decode(),
        cert_key=b64encode(pki.pem_encode_key(cert.key)).decode(),
    )
    