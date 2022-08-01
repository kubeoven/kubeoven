from kubeoven import ssh, templates, log

def create_containerd_conf(client: ssh.NodeClient, registry_node: str):
    dst = '/etc/containerd/config.toml'
    log.info(f'create {dst}')
    data = templates.render('containerd.toml.j2', registry_node=registry_node)
    client.write_file(dst, data)
