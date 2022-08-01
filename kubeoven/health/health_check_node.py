from paramiko import SSHClient
from kubeoven import conf, log
from .health_check_apiserver import health_check_apiserver
from .health_check_kubelet import health_check_kubelet
from .health_check_scheduler import health_check_scheduler
from .health_check_ctrl_manager import health_check_ctrl_mgr
from .health_check_nginx_proxy import health_check_nginx_proxy


def health_check_control_node(node: conf.NodeConf, client: SSHClient):
    log.info('wait for kublet readiness')
    health_check_kubelet(client)
    log.info('wait for kube-apiserver readiness')
    health_check_apiserver(client)
    log.info('wait for kube-scheduler readiness')
    health_check_scheduler(client)
    log.info('wait for kube-controller-manager readiness')
    health_check_ctrl_mgr(client)


def health_check_worker_node(node: conf.NodeConf, client: SSHClient):
    log.info('wait for kublet readiness')
    health_check_kubelet(client)
    log.info('wait for nginx proxy readiness')
    health_check_nginx_proxy(client)

