from kubeoven import log, conf, ssh, pki
from cryptography import x509

def create_scheduler_kubeconf(
    ca: pki.KeyPair,
    cert: pki.KeyPair,
    client: ssh.NodeClient
):
    dst = '/etc/kubernetes/scheduler.conf'
    log.info(f'write {dst}')
    user = "system:kube-scheduler"
    data = conf.create_kubeconfig(ca, cert, user)
    client.write_file(dst, data)
