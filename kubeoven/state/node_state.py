from pydantic import Field, BaseModel
from .process_state import ProcessState
from kubeoven.conf import NodeConf


class NodeState(BaseModel):
    config: NodeConf
    containerd: ProcessState = Field(default_factory=ProcessState)
    etcd: ProcessState = Field(default_factory=ProcessState)
    nginx_proxy: ProcessState = Field(default_factory=ProcessState)
    kubelet: ProcessState = Field(default_factory=ProcessState)
    kube_apiserver: ProcessState = Field(default_factory=ProcessState)
    kube_controller_manager: ProcessState = Field(default_factory=ProcessState)
    kube_scheduler: ProcessState = Field(default_factory=ProcessState)
    cache_server: ProcessState = Field(default_factory=ProcessState)
    registry: ProcessState = Field(default_factory=ProcessState)
