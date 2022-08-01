from kubeoven import log, ssh, templates
from kubeoven.conf import ClusterConf
from kubeoven.constants import K8S_GCR_REGISTRY


def create_ctrl_mgr_manifest(config: ClusterConf, client: ssh.NodeClient):
    dst = "/etc/kubernetes/manifests/kube-controller-manager.yaml"
    log.info(f"write {dst}")
    src = "kube_controller_manager.yaml.j2"
    data = templates.render(
        src,
        version=config.kubernetes_version,
        cluster_cidr=config.cluster_cidr,
        registry=config.registry_uri(K8S_GCR_REGISTRY),
    )
    client.write_file(dst, data)
