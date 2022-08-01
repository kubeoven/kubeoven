from kubeoven.conf import ClusterConf
from kubeoven.state import FullState, get_present_controlplane_node, Manifest
from kubeoven.ssh import NodeClient, create_node_client
import os

def deploy_manifests(full_state: FullState):
    addr = get_present_controlplane_node(full_state)
    with create_node_client(full_state, addr) as client:
        # unapply_manifests(full_state, client)
        apply_manifests(full_state, client)


def apply_manifests(full: FullState, client: NodeClient):
    for manifest in full.next.manifests:
        if manifest not in full.current.manifests:
            deploy(client, manifest, full.config)
            full.current.manifests.append(manifest)
            full.current.commit()


def deploy(client: NodeClient, manifest: Manifest, cluster: ClusterConf):
    dst = os.path.join('/tmp/', os.path.basename(manifest.path))
    client.write_file(dst, manifest.build(cluster))
    kubeconfig = "/etc/kubernetes/admin.conf"
    client.exec_command(f"kubectl apply --kubeconfig {kubeconfig} -f {dst}")

# def unapply_manifests(full: FullState, client: NodeClient):
#     for manifest in full.current.manifests:
#         if manifest not in full.next.manifests:
#             undeploy(client, manifest)
#             full.current.manifests.remove(manifest)
#             full.current.commit()

# def undeploy(client: NodeClient, manifest: Manifest):
#     dst = os.path.join('/tmp/', os.path.basename(manifest.path))
#     client.write_file(dst, manifest.get())
#     kubeconfig = "/etc/kubernetes/admin.conf"
#     client.exec_command(f"kubectl delete --kubeconfig {kubeconfig} -f {dst}")

