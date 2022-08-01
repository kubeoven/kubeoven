from kubeoven import ssh, templates

def create_cache_service(client: ssh.NodeClient):
    content = templates.render("cache_server.service.j2")
    client.write_file('/etc/systemd/system/kubeoven-cache.service', content)
    client.exec_command('sudo systemctl daemon-reload')

