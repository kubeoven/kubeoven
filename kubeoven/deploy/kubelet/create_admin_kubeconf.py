from  base64 import b64encode
from kubeoven import log, pki, ssh, templates

def create_admin_kubeconf(ca: pki.KeyPair, client: ssh.NodeClient):
    dst = '/etc/kubernetes/admin.conf'
    log.info(f'write {dst}')
    user = "kubernetes-admin"
    cert= create_admin_certs(user, ca)
    data = templates.render(
        "kubeconfig.yaml.j2",
        user=user,
        ca_cert=b64encode(pki.pem_encode_cert(ca.cert)).decode(),
        cert=b64encode(pki.pem_encode_cert(cert.cert)).decode(),
        cert_key=b64encode(pki.pem_encode_key(cert.key)).decode(),
    )
    client.write_file(dst, data)


def create_admin_certs(cn: str, ca: pki.KeyPair):
    log.info('create admin certs')
    return pki.create_cert(
        ca=ca,
        cn=cn,
        org="system:masters",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageBoth,
    )