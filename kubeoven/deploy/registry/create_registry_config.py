from kubeoven import templates, log
from kubeoven.ssh import NodeClient


def create_registry_config(client: NodeClient):
    dst = '/etc/docker/registry/config.yaml'
    log.info(f'write {dst}')
    data = templates.render('registry.yaml.j2')
    client.write_file(dst, data)

