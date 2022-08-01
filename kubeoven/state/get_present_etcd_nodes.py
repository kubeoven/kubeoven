from typing import List, Optional, Set
from .full_state import FullState

def get_present_etcd_nodes(full_state:FullState) -> List[str]:
    values:Set[str] = set()
    for address in full_state.resources_keys():
        current, next = full_state.get_node_states(address)
        if next.etcd == current.etcd and next.etcd.is_present():
            values.add(address)
        elif current.etcd.is_present():
            values.add(address)
    return list(values)

def get_present_etcd_node(full_state:FullState) -> Optional[str] :
    nodes = get_present_etcd_nodes(full_state)
    return nodes[0] if len(nodes) > 0 else None