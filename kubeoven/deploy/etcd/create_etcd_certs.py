from kubeoven import conf, log, pki, ssh


def create_etcd_certs(ca: pki.KeyPair, node: conf.NodeConf, client: ssh.NodeClient):
    dst = "/etc/kubernetes/pki"
    server = create_server_cert(ca, node)
    _client = create_client_cert(ca)
    log.info(f"write etcd certs {dst}/etcd")
    client.write_file(f"{dst}/ca.crt", pki.pem_encode_cert(ca.cert))
    client.write_file(f"{dst}/ca.key", pki.pem_encode_key(ca.key))
    client.write_file(f"{dst}/etcd/server.crt", pki.pem_encode_cert(server.cert))
    client.write_file(f"{dst}/etcd/server.key", pki.pem_encode_key(server.key))
    client.write_file(f"{dst}/etcd/client.crt", pki.pem_encode_cert(_client.cert))
    client.write_file(f"{dst}/etcd/client.key", pki.pem_encode_key(_client.key))


def create_server_cert(ca: pki.KeyPair, node: conf.NodeConf):
    log.info("create etcd server certs")
    dns = [node.hostname or "", "localhost"]
    addresses = [node.address, "127.0.0.1"]
    return pki.create_cert(
        ca=ca,
        cn="kube-etcd",
        org="",
        addresses=addresses,
        dns=dns,
        key_usage=pki.KeyUsageBoth,
    )


def create_client_cert(ca: pki.KeyPair):
    log.info("create etcd client certs")
    return pki.create_cert(
        ca=ca,
        cn="kube-etcd-healthcheck-client",
        org="",
        addresses=[],
        dns=[],
        key_usage=pki.KeyUsageClient,
    )


