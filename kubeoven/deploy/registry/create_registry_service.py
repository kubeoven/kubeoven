from kubeoven.ssh import NodeClient
from kubeoven import templates, log

def create_registry_service(client: NodeClient):
    dst = '/etc/systemd/system/registry.service'
    log.info(f'write {dst}')
    data = templates.render('registry.service.j2')
    client.write_file(dst, data)
    client.exec_command('sudo systemctl daemon-reload')
