from kubeoven import ssh, templates, log

def create_containerd_service(client: ssh.NodeClient):
    dst = '/etc/systemd/system/containerd.service'
    log.info(f'write {dst}')
    data = templates.render('containerd.service.j2')
    client.write_file(dst, data)
    client.exec_command('sudo systemctl daemon-reload')

