from kubeoven import state, templates
from kubeoven.state import FullState
from kubeoven.ssh import NodeClient


def create_kube_proxy_manifest(full_state: FullState, client: NodeClient):
    config = full_state.config
    address = state.get_present_controlplane_node(full_state)
    data = templates.render(
        "kube_proxy_ds.yaml.j2",
        version=config.kubernetes_version,
        address=address,
        cluster_cidr=config.cluster_cidr
    )
    dst = "/var/lib/kube-proxy/kube-proxy-ds.yaml"
    admin = "/etc/kubernetes/admin.conf"
    client.write_file(dst, data)
    client.exec_command(f"kubectl apply --kubeconfig {admin} -f {dst}")

