from kubeoven import pki, log
from kubeoven.pki import KeyPair


def create_scheduler_certs(ca: KeyPair):
    log.info('create kube-scheduler certs')
    return pki.create_cert(
        ca=ca,
        cn="system:kube-scheduler",
        org="",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageBoth,
    )