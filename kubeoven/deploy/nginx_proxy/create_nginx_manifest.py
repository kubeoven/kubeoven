from kubeoven import ssh, templates


def create_nginx_manifest(conf_hash:str, client:ssh.NodeClient):
    dst = '/etc/kubernetes/manifests/nginx-proxy.yaml'
    content = templates.render('nginx_proxy.yml.j2', conf_hash=conf_hash)
    client.write_file(dst, content)

