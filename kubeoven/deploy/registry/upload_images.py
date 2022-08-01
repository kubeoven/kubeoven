from kubeoven import ssh
from kubeoven.state import FullState
from kubeoven.constants import IMAGES_DIR, CRANE_CLI
from kubeoven.exceptions import AppException
from .get_images_refs import get_images_refs
import subprocess
import os

def upload_images(full_state: FullState):
    addr = full_state.config.registry_node()
    with ssh.create_node_client(full_state, addr) as client:
        with ssh.forward(addr, 5000, client.ssh) as f:
            url = f"{f.server_address[0]}:{f.server_address[1]}"
            images = get_images_refs(full_state)
            for ref in images:
                dst = os.path.join(IMAGES_DIR, ref.registry, ref.name + '.tar.gz' )
                cmd = [CRANE_CLI, "push", dst, f"{url}/{ref.name}", "--insecure"]
                output = subprocess.run(cmd, capture_output=True)
                if output.returncode != 0:
                   raise AppException(output.stderr.decode())
