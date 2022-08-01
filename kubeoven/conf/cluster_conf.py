from typing import List, Optional
from semver import VersionInfo
from pydantic import BaseModel, Field
from .containerd_versions import containerd_versions
from .node_conf import NodeConf
from .bastion_conf import BastionConf
from .network_conf import NetworkConf
import ipaddress


class ClusterConf(BaseModel):
    bastion_host: Optional[BastionConf] = Field(default=None)
    kubernetes_version: str = Field()
    nodes: List[NodeConf] = Field(min_items=1)
    network: NetworkConf = Field(default_factory=NetworkConf)

    @property
    def os(self):
        return "linux"

    @property
    def arch(self):
        return ["x86_64"]

    @property
    def cni_plugins_version(self):
        return "v1.0.1"

    @property
    def etcd_version(self):
        return "v3.5.2"

    @property
    def min_etcd_version(self):
        return "v3.2.18"

    @property
    def registry_version(self):
        return 'v2.8.1'

    @property
    def go_containerregistry_version(self):
        return 'v0.11.0'

    @property
    def nginx_proxy_version(self):
        return '1.21'

    @property
    def containerd_version(self):
        ver = VersionInfo.parse(self.kubernetes_version.replace("v", ""))
        key = f"v{ver.major}.{ver.minor}"
        found = containerd_versions.get(key, None)
        if found is None:
            raise RuntimeError(
                f"no supported containerd version found for {self.kubernetes_version}"
            )
        return found

    @property
    def runc_version(self):
        return "v1.1.0"

    @property
    def etcd_nodes(self):
        return [n.address for n in self.nodes if "etcd" in n.role]

    @property
    def etcd_servers(self):
        return [f"https://{addr}:2379" for addr in self.etcd_nodes]

    @property
    def controlplane_nodes(self):
        return [n.address for n in self.nodes if "controlplane" in n.role]

    @property
    def cache_server(self):
        for node in self.nodes:
            if "cache" in node.role:
                return node.address
        return None

    @property
    def cluster_cidr(self):
        return "192.168.0.0/16"


    def registry_node(self):
        for node in self.nodes:
            if 'registry' in node.role:
                return node.address
        return None
        
    def registry_uri(self, default=""):
        addr = self.registry_node()
        if addr:
            return f'{addr}:5000'
        return default

    def controlplane_node(self) -> str:
        nodes = self.controlplane_nodes
        nodes = sorted(nodes, key=ipaddress.IPv4Address)
        return nodes[0]

    def get_node_config(self, address: str):
        for node in self.nodes:
            if node.address == address:
                return node
        raise RuntimeError(f"no node config for {address}")
