from typing import List, Optional, Set
from .full_state import FullState

def get_present_kubelet_nodes(full_state:FullState) -> List[str]:
    values:Set[str] = set()
    for address in full_state.resources_keys():
        current, next = full_state.get_node_states(address)
        if next.kubelet.is_present() and next.kubelet == current.kubelet:
            values.add(address)
        elif current.kubelet.is_present():
            values.add(address)
    return list(values)

def get_present_kubelet_node(full_state:FullState) -> Optional[str] :
    nodes = get_present_kubelet_nodes(full_state)
    return nodes[0] if len(nodes) > 0 else None