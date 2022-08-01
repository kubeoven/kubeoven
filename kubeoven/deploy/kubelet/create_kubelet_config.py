from kubeoven import templates, ssh, log

def create_kubelet_config(client: ssh.NodeClient):
    dst = '/var/lib/kubelet/kubelet-config.yaml'
    log.info(f'write {dst}')
    data = templates.render('kubelet_config.yaml.j2')
    client.write_file(dst, data.encode())
