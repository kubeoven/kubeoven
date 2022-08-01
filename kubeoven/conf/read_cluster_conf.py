import os
import yaml
from pathlib import Path
from kubeoven.conf import ClusterConf
from kubeoven import log
from pydantic import ValidationError
from kubeoven.exceptions import AppException

def read_cluster_conf(dst: str):
    dst = get_cluster_conf_file(dst)
    log.info('reading cluster config')
    try:
        ext = Path(dst).suffix
        if ext == '.py':
            return read_cluster_py_conf('cluster.py')
        else:
            return read_cluster_yaml_conf(dst)
    except ValidationError as error:
        log.error(f'found problems in {dst}')
        raise format_validation_error(error)

def get_cluster_conf_file(dst: str):
    cur  = os.getcwd()
    if dst != "":
        return dst
    if os.path.exists(os.path.join(cur, 'cluster.yml')):
        return 'cluster.yml'
    if os.path.exists(os.path.join(cur, 'cluster.yaml')):
        return 'cluster.yaml'
    if os.path.exists(os.path.join(cur, 'cluster.py')):
        return 'cluster.py'
    raise AppException('not cluster config file found')

def read_cluster_yaml_conf(dst: str):
    source = Path(dst).read_text()
    val = yaml.safe_load(source)
    return ClusterConf(**val)


def read_cluster_py_conf(dst):
    locals = {}
    exec(open(dst).read(), {}, locals)
    func = locals.get('main', None)
    if func is None:
        raise AppException(f'no main def found in {dst}')
    val = func() or {}
    return ClusterConf(**val)

def format_validation_error(error: ValidationError):
    messages = []
    for err in error.errors():
        loc = ".".join([str(p) for p in err['loc']])
        msg = f"path '{loc}' {err['msg']}"
        messages.append(msg)
    return AppException(*messages)
