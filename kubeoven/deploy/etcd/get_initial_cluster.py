from typing import List
from kubeoven.state import FullState


def get_initial_cluster(full_state: FullState) -> List[str]:
    values:List[str] = []
    for key in full_state.resources_keys():
        current, next = full_state.get_node_states(key)
        if current.etcd.is_present(): 
            config = current.config
            val = f"{config.hostname}=https://{config.address}:2380"
            values.append(val)
    return values
