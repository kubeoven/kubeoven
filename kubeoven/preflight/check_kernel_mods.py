from typing import List
from kubeoven import ssh
from kubeoven import templates
from kubeoven.exceptions import AppException
from kubeoven.ssh.node_client import CommandError


def check_kernel_mods(client: ssh.NodeClient):
    mods = ['br_netfilter', 'overlay']
    disabled = kernel_mod_disabled(client, mods)
    if disabled is None:
        return
    disabled = enable_kernel_mods(client, mods)
    if disabled is None:
        return
    raise AppException(f'kernel mod {disabled[0]} not enabled', hostname=client.hostname)
    
def enable_kernel_mods(client: ssh.NodeClient, mods: List[str]):
    dst = '/etc/modules-load.d/k8s.conf'
    data = templates.render('modules_load.conf.j2')
    client.write_file(dst, data)
    client.exec_command(f'sudo modprobe --all ' + " ".join(mods))
    return kernel_mod_disabled(client, mods)

def kernel_mod_disabled(client: ssh.NodeClient, mods: List[str]):
    for mod in mods:
        try:
            client.exec_command(f'cat /proc/modules | grep {mod}')
        except CommandError:
            return mod
    return None
            