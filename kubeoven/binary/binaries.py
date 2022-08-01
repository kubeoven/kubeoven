from .binary import Binary
from kubeoven.templates import render_string
from kubeoven.common import to_amd
from typing import Dict, List, TypedDict
from os import path
from kubeoven.conf import ClusterConf
import platform

def get_binary(name: str, version: str, os: str, arch: str):
    bin = bins[name]
    url = render_string(bin['url'], version=version[1:], os=os, arch=arch)
    return Binary(
        url=url,
        filename=path.basename(url),
        version=version,
        sha256=bin['sha256']['_'.join([version, os, arch])]
    )

def get_binaries(cluster: ClusterConf):
    bins:List[Binary] = []
    registry_node = cluster.registry_node()
    for arch in cluster.arch:
        bins = bins + [
            get_binary("cni-plugins", cluster.cni_plugins_version, "linux", to_amd(arch)),
            get_binary("kubectl", cluster.kubernetes_version, "linux", to_amd(arch)),
            get_binary("kubelet", cluster.kubernetes_version, "linux", to_amd(arch)),
            get_binary("containerd", cluster.containerd_version, "linux", to_amd(arch)),
            get_binary("runc", cluster.runc_version, "linux", to_amd(arch)),
            get_binary("crictl", cluster.kubernetes_version, "linux", to_amd(arch)),
            get_binary("etcd", cluster.etcd_version, "linux", to_amd(arch)),
        ]
        if(registry_node):
            bins = bins + [
                get_binary('registry', cluster.registry_version, 'linux', to_amd(arch)),
                get_binary('go-containerregistry', cluster.go_containerregistry_version, platform.system().lower(), platform.machine())
            ]
    return bins

BinInfo = TypedDict('BinInfo', {'url': str, 'sha256': Dict[str, str], 'alias': Dict[str, str]}, total=False)

bins:Dict[str, BinInfo] = {
    'caddy': {
        'url': "https://github.com/caddyserver/caddy/releases/download/v{{ version}}/caddy_{{ version }}_{{ os }}_{{ arch }}.tar.gz",
        'sha256': {
            'v2.4.6_linux_amd64': '690ad64538a39d555294cd09b26bb22ade36abc0e3212342f0ed151de51ec128'
        },
    },
    'etcd': {
        'url': 'https://github.com/etcd-io/etcd/releases/download/v{{ version }}/etcd-v{{ version }}-{{ os }}-{{ arch }}.tar.gz',
        'sha256': {
            'v3.5.2_linux_amd64': '256cad725542d6fd463e81b8a19b86ead4cdfe113f7fb8a1eabc6c32c25d068b'
        }
    }, 
    'kubelet': {
        'url': 'https://storage.googleapis.com/kubernetes-release/release/v{{ version }}/bin/{{ os }}/{{ arch }}/kubelet',
        'sha256': {
            'v1.20.0_linux_amd64': 'ff2422571c4c1e9696e367f5f25466b96fb6e501f28aed29f414b1524a52dea0'
        }
    },
    'kubectl': {
        'url': 'https://storage.googleapis.com/kubernetes-release/release/v{{ version }}/bin/{{ os }}/{{ arch }}/kubectl',
        'sha256': {
            'v1.20.0_linux_amd64': 'a5895007f331f08d2e082eb12458764949559f30bcc5beae26c38f3e2724262c'
        }
    },
    'containerd': {
        'url': 'https://github.com/containerd/containerd/releases/download/v{{ version }}/containerd-{{ version }}-{{ os }}-{{ arch }}.tar.gz',
        'sha256': {
            'v1.5.13_linux_amd64': '7b5b34f30a144985e849bdeb0921cfd3fe65f9508b5707fd237fd2c308d9abae'
        }
    },
    'runc': {
        'url': 'https://github.com/opencontainers/runc/releases/download/v{{ version }}/runc.{{ arch }}',
        'sha256': {
            'v1.1.0_linux_amd64': 'ab1c67fbcbdddbe481e48a55cf0ef9a86b38b166b5079e0010737fd87d7454bb'
        }
    },
    'cni-plugins': {
        'url': 'https://github.com/containernetworking/plugins/releases/download/v{{ version }}/cni-plugins-{{ os }}-{{ arch }}-v{{ version }}.tgz',
        'sha256': {
            'v1.0.1_linux_amd64': '5238fbb2767cbf6aae736ad97a7aa29167525dcd405196dfbc064672a730d3cf'
        }
    },
    'crictl': {
        'url': 'https://github.com/kubernetes-sigs/cri-tools/releases/download/v{{ version }}/crictl-v{{ version }}-{{ os }}-{{ arch }}.tar.gz',
        'sha256': {
            'v1.20.0_linux_amd64': '44d5f550ef3f41f9b53155906e0229ffdbee4b19452b4df540265e29572b899c'
        }
    },
    'registry': {
        'url': 'https://github.com/distribution/distribution/releases/download/v{{ version }}/registry_{{ version }}_{{ os }}_{{ arch }}.tar.gz',
        'sha256': {
            'v2.8.1_linux_amd64': 'f1a376964912a5fd7d588107ebe5185da77803244e15476d483c945959347ee2'
        }
    },
    'go-containerregistry': {
        'url': 'https://github.com/google/go-containerregistry/releases/download/v{{ version }}/go-containerregistry_{{ os | capitalize }}_{{ arch }}.tar.gz',
        'sha256': {
            'v0.11.0_linux_x86_64': '3cec40eb0fac2e6ed4b71de682ae562d15819ab92145e4f669b57baf04797adb',
            'v0.11.0_darwin_x86_64': 'c7b2d619f465a4a877e431641ccc1c905583cf212f596b9bce681691637b3ef6'
        }
    }
}

