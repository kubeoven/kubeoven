import click
from kubeoven.binary import download_binaries
from kubeoven.conf import read_cluster_conf
from kubeoven import state, log, ssh, conf
from kubeoven.state import FullState
from kubeoven.deploy import deploy_cluster

@click.command(name="clean", help='clean k8s nodes using cluster.yml file')
@click.argument('file', type=click.Path(exists=True), default="cluster.yml")
def clean_command(file: str):
    log.set_hostname('localhost')
    config = read_cluster_conf(file)
    current = state.get_current_state()
    next = state.build_next_state(config)
    full_state = FullState(next, current)
    ssh.provide_bastion_client(config.bastion_host)
    for addr in full_state.resources_keys():
        addr = full_state.get_node_conf(addr)


def clean_node(node: conf.NodeConf):
    with ssh.create_node_client(node) as client:
        client.exec_command("")
        pass