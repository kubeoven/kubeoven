import hashlib
from kubeoven import ssh, templates
from typing import List

def create_nginx_config(addresses: List[str], client: ssh.NodeClient) -> str:
    content = templates.render("nginx.conf.j2", addresses=addresses)
    client.write_file('/etc/kubernetes/nginx-proxy/nginx.conf', content)
    hash = hashlib.sha256()
    hash.update(content.encode())
    return hash.hexdigest()
