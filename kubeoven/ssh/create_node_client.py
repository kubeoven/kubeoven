from contextlib import contextmanager
from kubeoven import state
from paramiko import AutoAddPolicy, SFTPClient, SSHClient, Channel
from .node_client import NodeClient


@contextmanager
def create_node_client(full_state: state.FullState, address: str):
    node, bastion = full_state.get_node_conf(address)
    if bastion:
        bastion_client = create_ssh_client(bastion.user, bastion.address, bastion.port)
        sock = bastion_client.get_transport().open_channel(
            "direct-tcpip", (node.address, node.port), (bastion.address, bastion.port)
        )
        client = create_ssh_client(node.user, node.address, node.port, sock)
        sftp_client = create_sftp_client(client)
        try:
            yield NodeClient(client, sftp_client, node.hostname)
        finally:
            client.close()
            bastion_client.close()
    else:
        client = create_ssh_client(node.user, node.address, node.port)
        sftp_client = create_sftp_client(client)
        try:
            yield NodeClient(client, sftp_client, node.hostname)
        finally:
            client.close()


def create_ssh_client(username: str, address: str, port: int, sock: Channel = None):
    ssh_client = SSHClient()
    ssh_client.load_system_host_keys()
    ssh_client.set_missing_host_key_policy(AutoAddPolicy())
    ssh_client.connect(address, port, sock=sock, username=username)
    return ssh_client


def create_sftp_client(client: SSHClient):
    transport = client.get_transport()
    if transport is None:
        raise RuntimeError("unable to create sftp client no transport found")
    chan = transport.open_channel("session")
    chan.exec_command("sudo /usr/lib/openssh/sftp-server")
    sftp = SFTPClient(chan)
    return sftp
