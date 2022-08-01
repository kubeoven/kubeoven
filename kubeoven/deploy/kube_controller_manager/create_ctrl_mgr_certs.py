from kubeoven import pki, log
from kubeoven.pki import KeyPair

def create_ctrl_mgr_certs(ca: KeyPair):
    log.info('create kube-controller-manager certs')
    return pki.create_cert(
        ca=ca,
        cn="system:kube-controller-manager",
        org="",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageBoth,
    )
