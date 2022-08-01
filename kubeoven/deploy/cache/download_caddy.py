import os
from kubeoven import binary, ssh
from kubeoven.binary import upload_binary_to_node

CADDY_VERSION = 'v2.4.6'

def download_caddy(client: ssh.NodeClient):
    bin = binary.get_binary('caddy', CADDY_VERSION, "linux", "amd64")
    bin = binary.download_binary(bin)
    dst = os.path.join('/tmp', bin.filename)
    upload_binary_to_node(bin, dst, client)
    cmd = f"tar -xvf {dst} --directory=/usr/local/bin caddy"
    client.exec_command(f"sudo {cmd}")
