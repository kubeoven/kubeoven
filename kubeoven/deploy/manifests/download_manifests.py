from kubeoven.state import ClusterState
from kubeoven.constants import KUBEOVEN_DIR
import os

def download_manifests(state: ClusterState):
    os.makedirs(os.path.join(KUBEOVEN_DIR, 'manifests'), 0o775, exist_ok=True)
    for manifest in state.manifests:
        manifest.download()
    
    

