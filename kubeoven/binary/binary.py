import os
from dataclasses import dataclass


@dataclass
class Binary():
    url: str
    sha256: str
    filename: str
    version: str

    def path(self, base_dir:str=None):
        if base_dir is None:
            base_dir = os.path.join(os.getcwd(), '.kubeoven', 'cache')
        return os.path.join(base_dir, self.version, self.filename)
