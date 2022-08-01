from kubeoven.conf.cluster_conf import ClusterConf
from kubeoven import log, ssh, templates
from kubeoven.constants import K8S_GCR_REGISTRY


def create_scheduler_manifest(cluster: ClusterConf, client: ssh.NodeClient):
    dst = "/etc/kubernetes/manifests/kube-scheduler.yaml"
    log.info(f"write {dst}")
    src = "kube_scheduler.yaml.j2"
    data = templates.render(
        src,
        version=cluster.kubernetes_version,
        registry=cluster.registry_uri(K8S_GCR_REGISTRY),
    )
    client.write_file(dst, data)
