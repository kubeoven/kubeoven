from typing import Dict, Set, cast
from pydantic import BaseModel, Field
import semver

class Status():
    ABSENT = 'ABSENT'
    PRESENT = 'PRESENT'

class ProcessState(BaseModel):
    version: str = Field(default="")
    status: str = Field(default=Status.ABSENT)
    depends: Set[str] = Field(default_factory=set)

    def is_present(self):
        return self.status == Status.PRESENT

    def should_deploy(self, next: 'ProcessState'):
        c1 = self.status == Status.ABSENT
        c2 = next.status == Status.PRESENT
        return c1 and c2

    def should_upgrade(self, next: 'ProcessState'):
        c1 = self.is_present() and next.is_present()
        c2 = semver.compare(next.version, self.version) == 1
        c3 = self.depends != next.depends
        return c1 and (c2 or c3)
    
    def should_undeploy(self, next: 'ProcessState'):
        c1 = self.is_present()
        c2 = not next.is_present()
        return c1 and c2
        