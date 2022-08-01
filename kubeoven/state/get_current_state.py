import os
import json
import click
from kubeoven import conf
from kubeoven import log
from .full_state import ClusterState

def get_current_state(cluster: conf.ClusterConf) -> ClusterState:
    log.info('reading current state')
    path = os.path.join(os.getcwd(), ".kubeoven", "state.json")
    try:
        with open(path) as file:
            content = file.read()
            if len(content) == 0:
                raise FileNotFoundError()
            data = json.loads(content)
            return ClusterState(**data)
    except FileNotFoundError:
        return ClusterState(resources=dict())
    except json.JSONDecodeError:
        log.error('state file corrupted')
        raise click.Abort
