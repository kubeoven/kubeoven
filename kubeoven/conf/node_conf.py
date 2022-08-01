from typing import Optional, List

from pydantic import BaseModel, Field

# node-role.kubernetes.io/master:NoSchedule

Roles = {
    "controlplane": [
        "node-role.kubernetes.io/master=master",
        "node-role.kubernetes.io/control-plane=control-plane",
    ],
    "worker": ["node-role.kubernetes.io/worker=worker"],
}


class NodeConf(BaseModel):
    address: str = Field()
    user: Optional[str] = Field(default=None)
    hostname_override: Optional[str] = Field(default=None)
    port: int = Field(default=22)
    role: List[str] = Field(default_factory=list)

    @property
    def hostname(self):
        return self.hostname_override or self.address

    def labels(self) -> List[str]:
        labels: List[str] = []
        for role in self.role:
            labels = labels + Roles.get(role, [])
        return labels
