import re
from typing import List
from kubeoven.state import FullState, Manifest
from .image_ref import ImageRef

def get_images_refs(full_state: FullState):
    cluster = full_state.config
    refs = [
        ImageRef.of(f"nginx:{cluster.nginx_proxy_version}"),
        ImageRef.of(f"k8s.gcr.io/kube-proxy:{cluster.kubernetes_version}"),
        ImageRef.of(f"k8s.gcr.io/kube-apiserver:{cluster.kubernetes_version}"),
        ImageRef.of(f"k8s.gcr.io/kube-scheduler:{cluster.kubernetes_version}"),
        ImageRef.of(f"k8s.gcr.io/kube-controller-manager:{cluster.kubernetes_version}")
    ]
    refs = refs + get_images_from_manifests(full_state.next.manifests)
    return refs


def get_images_from_manifests(manifests: List[Manifest]):
    pattern = '(?<=image:).*$'
    refs:List[ImageRef] = []
    for manifest in manifests:
        content = manifest.get()
        matches:List[str] = re.findall(pattern, content)
        for match in matches:
            refs.append(ImageRef.of(match.strip()))
    return refs
