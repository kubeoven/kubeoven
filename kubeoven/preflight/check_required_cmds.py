from kubeoven import ssh
from kubeoven.exceptions import AppException

def check_required_cmds(client:ssh.NodeClient):
    cmds = ['conntrack', 'ip', 'iptables', 'mount', 'nsenter']
    for cmd in cmds:
        if not client.command_exists(cmd):
            msg = f"{cmd} not found in path"
            raise AppException(msg, hostname=client.hostname)
