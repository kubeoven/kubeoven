import click
from kubeoven.binary import download_binaries
from kubeoven.conf import read_cluster_conf
from kubeoven import state, log, preflight
from kubeoven.state import FullState
from kubeoven.deploy import deploy_cluster
from kubeoven.deploy.manifests import download_manifests


@click.command(name="deploy", help='deploy k8s using cluster.yml file')
@click.argument('file', default="")
def deploy_command(file: str):
    log.set_hostname('localhost')
    cluster = read_cluster_conf(file)
    current = state.get_current_state(cluster)
    next = state.build_next_state(cluster)
    if current == next:
        return
    full_state = FullState(next=next, current=current, config=cluster)
    download_binaries(cluster)
    download_manifests(next)
    preflight.check_nodes(full_state)
    deploy_cluster(full_state)
    log.set_hostname('localhost')
    log.info('all done!')
