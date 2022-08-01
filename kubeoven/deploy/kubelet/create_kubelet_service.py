from kubeoven import ssh, log, templates, conf

def create_kubelet_service(client: ssh.NodeClient, node: conf.NodeConf):
    dst = '/etc/systemd/system/kubelet.service'
    log.info(f'write {dst}')
    data = templates.render('kubelet.service.j2', hostname=node.hostname)
    client.write_file(dst, data)
    client.exec_command('sudo systemctl daemon-reload')
    