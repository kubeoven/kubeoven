from kubeoven import log
from kubeoven.state import FullState
from kubeoven.conf import ClusterConf
from kubeoven.constants import IMAGES_DIR, CRANE_CLI
from kubeoven.binary import get_binary
from kubeoven.exceptions import AppException
from .get_images_refs import get_images_refs
import subprocess
import platform
import tarfile
import os

def download_images(full_state:FullState):
    images = get_images_refs(full_state)
    for ref in images:
        dst = os.path.join(IMAGES_DIR, ref.registry, ref.name + '.tar.gz' )
        try: 
            os.stat(dst)
        except FileNotFoundError:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            cmd = [CRANE_CLI, "pull", str(ref), dst]
            log.info(f'pulling {str(ref)}')
            output = subprocess.run(cmd, capture_output=True)
            if output.returncode != 0:
                raise AppException(output.stderr.decode())


def ensure_crane_cli(cluster: ClusterConf):
    bin = get_binary('go-containerregistry', cluster.go_containerregistry_version, platform.system().lower(), platform.machine())
    with tarfile.open(bin.path()) as file:
        dst = os.path.dirname(CRANE_CLI)
        file.extract('crane', dst)
