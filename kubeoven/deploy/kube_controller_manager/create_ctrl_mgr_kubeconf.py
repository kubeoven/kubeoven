from paramiko import SFTPClient
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa
from kubeoven import log, conf, ssh, pki

def create_ctrl_mgr_kubeconf(
    ca: pki.KeyPair,
    cert: pki.KeyPair,
    client: ssh.NodeClient,
):
    dst = '/etc/kubernetes/controller-manager.conf'
    log.info(f'write {dst}')
    user = "system:kube-controller-manager"
    data = conf.create_kubeconfig(ca, cert, user)
    client.write_file(dst, data)
