from typing import MutableMapping, Any
from kubeoven import ssh
import toml

# def check_container_runtime(client :ssh.NodeClient):
#     if not client.command_exists('conatinerd'):
#         return
#     client.is_service_running('containerd')
#     conf = get_containerd_conf(client, sftp)
#     if ensure_cgroup_driver(conf, sftp):
#         cmd = 'sudo systemctl restart containerd.service'
#         ssh.exec_command(cmd, client)

# def ensure_cgroup_driver(conf: MutableMapping[str, Any], sftp: SFTPClient)->bool:
#     plugins = conf.setdefault('plugins', {})
#     cri = plugins.setdefault('io.containerd.grpc.v1.cri', {})
#     containerd = cri.setdefault('containerd', {})
#     runtimes = containerd.setdefault('runtimes', {})
#     runc = runtimes.setdefault('runc', {})
#     options = runc.setdefault('options', {})
#     if options.get('SystemdCgroup'):
#         return False
#     options['SystemdCgroup'] = True
#     with sftp.open('/etc/containerd/config.toml', 'w') as file:
#         file.write(toml.dumps(conf))
#     return True

# def get_containerd_conf(client: SSHClient, sftp:SFTPClient)-> MutableMapping[str, Any]:
#     file_path = '/etc/containerd/config.toml'
#     try:
#         file = sftp.open(file_path)
#         return toml.loads(file.read().decode('utf-8'))
#     except FileNotFoundError:
#         _, stdout, _ = client.exec_command(f"containerd config default > {file_path}")
#         if stdout.channel.recv_exit_status() != 0:
#             raise RuntimeError("unable to write containerd default config")
#         return get_containerd_conf(client, sftp)

