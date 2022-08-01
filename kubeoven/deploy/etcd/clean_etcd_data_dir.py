from kubeoven import ssh, log
from kubeoven.ssh import NodeClient

def clean_etcd_data_dir(client: NodeClient):
    dst = '/var/lib/etcd'
    log.info(f'clean {dst}')
    client.exec_command(f'sudo sh -c "rm -rf /var/lib/etcd/*"')

