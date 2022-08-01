from typing import Dict, List
from pydantic import Field, BaseModel
from kubeoven.common import handle_extra_types
from .node_state import NodeState
from .manifest import Manifest
import os
import json

class ClusterState(BaseModel):
    resources: Dict[str, NodeState] = Field(default_factory=dict)
    manifests: List[Manifest] = Field(default_factory=list)

    def commit(self):
        path = os.path.join(os.getcwd(), ".kubeoven", "state.json")
        with open(path, "w") as file:
            content = json.dumps(self.dict(), indent=4, default=handle_extra_types)
            file.write(content)