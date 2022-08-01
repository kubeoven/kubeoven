from sshtunnel import open_tunnel, SSHTunnelForwarder

from kubeoven.conf import NodeConf, BastionConf


def create_ssh_tunnel(node: NodeConf, bastion: BastionConf)-> SSHTunnelForwarder:
    tunnel = open_tunnel(
        (bastion.address, bastion.port),
        ssh_username=bastion.user,
        ssh_pkey=bastion.ssh_key_path,
        remote_bind_address=(node.address, node.port),
    )
    tunnel.start()
    return tunnel

