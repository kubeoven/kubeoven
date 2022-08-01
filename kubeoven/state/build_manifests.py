from typing import List
from kubeoven.conf import ClusterConf
from .manifest import Manifest
from kubeoven import templates, constants
import os


def build_cluster_manifests(cluster: ClusterConf):
    manifests: List[Manifest] = []
    kube_proxy = build_kubeproxy_manifest(cluster)
    manifests.append(kube_proxy)
    network = build_network_manifest(cluster)
    if network:
        manifests.append(network)
    return manifests

def build_kubeproxy_manifest(cluster: ClusterConf):
    version = cluster.kubernetes_version
    data = templates.render(
        "kube_proxy_ds.yaml.j2",
        version=version,
        cluster_cidr=cluster.cluster_cidr,
        server=cluster.controlplane_node(),
        registry=cluster.registry_uri(constants.K8S_GCR_REGISTRY)
    )
    dst = os.path.join(".kubeoven", "cache", version, "kube-proxy.yaml")
    with open(dst, "w") as file:
        file.write(data)
    return Manifest(src=dst)


def build_network_manifest(cluster: ClusterConf):
    if cluster.network.plugin == "flannel":
        return Manifest(
            src="https://raw.githubusercontent.com/flannel-io/flannel/v0.19.0/Documentation/kube-flannel.yml",
            jq=[
                '''
                if ($registry != "") then 
                    (.[] | select(.kind == "DaemonSet").spec.template.spec.containers[].image |= $registry + "/" + .)
                else .[] end
                ''',
                '''
                if ($registry != "") then 
                    (.[] | select(.kind == "DaemonSet").spec.template.spec.initContainers[].image |= $registry + "/" + .)
                else .[] end''',
                '''
                .[] | select(.kind == "ConfigMap").data."net-conf.json" |= ({"Network": $cluster_cidr, "Backend": {"Type": "vxlan"}} | tostring)
                '''
                ]
        )
    return Manifest(src="")
