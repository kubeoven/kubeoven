from kubeoven import state, log, pki, ssh
from .full_state import FullState


def get_kube_ca(full_state: FullState):
    address = state.get_present_etcd_node(full_state)
    address = state.get_present_kubelet_node(full_state) if address is None else address
    if not address: 
        log.info('create kube certificate authority')
        ca_cert, ca_key = pki.create_ca('kube-ca')
        return pki.KeyPair(ca_cert, ca_key)
    with ssh.create_node_client(full_state, address) as client:
        cert_bytes = client.sftp.open('/etc/kubernetes/pki/ca.crt', 'r').read()
        key_bytes = client.sftp.open('/etc/kubernetes/pki/ca.key', 'r').read()
        cert = pki.pem_decode_cert(cert_bytes)
        cert_key = pki.pem_decode_key(key_bytes)
        return pki.KeyPair(cert, cert_key)
