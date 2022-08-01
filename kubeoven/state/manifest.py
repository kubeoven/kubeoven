from typing import List, Optional
from pydantic import Field, BaseModel
from kubeoven.constants import KUBEOVEN_DIR
from kubeoven.conf import ClusterConf
from hashlib import md5
from urllib import request
import shutil
import jq
import os
import yaml


class Manifest(BaseModel):

    src: str = Field()

    jq:List[str] = Field(default_factory=list)

    hash: str = Field(default="")

    @property
    def path(self):
        hash = md5(self.src.encode()).hexdigest()
        return os.path.join(KUBEOVEN_DIR, 'manifests', hash)

    def apply(self, src: str, config: ClusterConf):
        if not self.jq:
            return src
        args = {'registry': config.registry_uri(), 'cluster_cidr': config.cluster_cidr}
        data = list(yaml.safe_load_all(src))
        for trans in self.jq:
            data = jq.compile(trans, args=args).input(data).all()
        return str(yaml.dump_all(data, stream=None))

    def build(self, config: ClusterConf):
        with open(self.path, 'r') as file:
            return self.apply(file.read(), config)
    
    def download(self):
        dst = self.path
        if self.src.startswith('http'):
            request.urlretrieve(self.src, dst)
            return
        shutil.copy2(self.src, dst)
        self.hash = md5(open(dst,'rb').read()).hexdigest()
