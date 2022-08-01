from kubeoven.exceptions import AppException
from kubeoven import ssh, templates

def check_networking(client: ssh.NodeClient, configure=False):
    if configure:
        write_sysctl_conf(client)
    files = [
        '/proc/sys/net/ipv4/ip_forward',
        '/proc/sys/net/bridge/bridge-nf-call-iptables'
    ]
    for dst in files:
        if check_proc_file(client, dst):
            continue
        elif configure:
            raise AppException(f'{dst} != 1', hostname=client.hostname)
        else:
            return check_networking(client, True)

def write_sysctl_conf(client: ssh.NodeClient):
    data = templates.render('sysctl.conf.j2')
    client.write_file('/etc/sysctl.d/k8s.conf', data)
    client.exec_command('sudo sysctl --system')

def check_proc_file(client: ssh.NodeClient, dst: str):
    try:
        with client.sftp.open(dst) as file:
            data = file.read()
            return data.startswith(bytes('1', 'utf-8'))
    except FileNotFoundError:
        return False
