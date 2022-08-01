from kubeoven.conf import ClusterConf
from pydantic import BaseModel
from .node_state import NodeState
from .cluster_state import ClusterState


class FullState(BaseModel):
    config: ClusterConf
    next: ClusterState
    current: ClusterState

    def resources_keys(self):
        current = list(self.current.resources)
        next = list(self.next.resources)
        total = set(current + next)
        return list(total)

    def get_node_conf(self, address: str):
        bastion = self.config.bastion_host
        if address in self.next.resources:
            return self.next.resources[address].config, bastion
        if address in self.current.resources:
            return self.current.resources[address].config, bastion
        raise RuntimeError(f"no node config found for {address}")

    def get_node_states(self, address: str):
        node, _ = self.get_node_conf(address)
        current = self.current.resources.setdefault(address, NodeState(config=node))
        next = self.next.resources.setdefault(address, NodeState(config=node))
        return current, next

    def has_controlplane_changes(self, address: str):
        current, next = self.get_node_states(address)
        c1 = current.containerd != next.containerd
        c2 = current.kube_apiserver != next.kube_apiserver
        c3 = current.kube_controller_manager != next.kube_controller_manager
        c4 = current.kube_scheduler != next.kube_scheduler
        return c1 or c2 or c3 or c4

    def has_workerplane_changes(self, address: str):
        current, next = self.get_node_states(address)
        c1 = current.containerd != next.containerd
        c2 = current.kubelet != next.kubelet
        c3 = current.nginx_proxy != next.nginx_proxy
        return c1 or c2 or c3


