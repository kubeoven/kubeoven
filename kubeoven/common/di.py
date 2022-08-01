from dataclasses import dataclass
from typing import Dict, List, TypeVar, Type, Any

@dataclass
class InjectVal:
    instance: Any
    tags: List[str]

class InjectError(Exception):
    def __init__(self, t:Any, *tags:str) -> None:
        msg = 'unable to resolve value for {t} with tags {tags}'
        super().__init__(msg)

instances:Dict[Any, List[InjectVal]] = {}

def provide(instance:Any, *tags:str):
     vals = instances.setdefault(type(instance), list())
     val = InjectVal(instance, list(tags))
     vals.append(val)

T = TypeVar("T")

def inject(t:Type[T], *tags:str) -> T:
    values = instances.get(t, None)
    if values is None:
        raise InjectError(t, *tags)
    for val in values:
        if all(tag in val.tags for tag in tags):
            return val.instance
    raise InjectError(t, *tags)
