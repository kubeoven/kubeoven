from typing import List, Set
from .full_state import FullState

def get_present_controlplane_nodes(full_state:FullState) -> List[str]:
    values:Set[str] = set()
    for address in full_state.resources_keys():
        current, next = full_state.get_node_states(address)
        if current.kube_apiserver.is_present():
            values.add(address)
    return list(values)

def get_present_controlplane_node(full_state:FullState) -> str:
    nodes = get_present_controlplane_nodes(full_state)
    if len(nodes) > 0:
        return nodes[0]
    raise RuntimeError('no controlplane nodes found')
