import os
from typing import Tuple, Union
from paramiko import SSHClient, SFTPClient
from kubeoven.exceptions import CommandError

class NodeClient:

    ssh: SSHClient

    sftp: SFTPClient

    hostname: str

    os: str

    arch: str

    def __init__(self, ssh: SSHClient, sftp: SFTPClient, hostname: str = "") -> None:
        self.ssh = ssh
        self.sftp = sftp
        self.hostname = hostname
        out, _ = self.exec_command('uname -sm')
        (self.os, self.arch) = out.strip().lower().split(' ')

    def write_file(self, dst: str, content: Union[bytes, str]):
        self.ensure_dirs(os.path.dirname(dst))
        with self.sftp.open(dst, "w") as f:
            f.set_pipelined(True)
            f.write(content)

    def file_exists(self, path: str):
        try:
            self.sftp.stat(path)
            return True
        except FileNotFoundError:
            return False

    def command_exists(self, cmd: str) -> bool:
        _, stdout, _ = self.ssh.exec_command(f"command -v {cmd}")
        if stdout.channel.recv_exit_status() != 0:
            return False
        return True

    def exec_command(self, cmd: str) -> Tuple[str, int]:
        _, stdout, stderr = self.ssh.exec_command(cmd)
        exit_code = stdout.channel.recv_exit_status()
        if exit_code > 0:
            error = CommandError(exit_code, stderr.read().decode("utf-8"))
            raise error
        return stdout.read().decode("utf-8"), exit_code

    def ensure_dirs(self, *dirs: str):
        arg = " ".join(dirs)
        return self.exec_command(f"sudo mkdir -p {arg}")

    def is_service_running(self, service: str):
        _, code = self.exec_command(f"systemctl is-active {service}.service --quiet")
        return code == 0

    def stop_service(self, name: str):
        try:
            self.exec_command(f"sudo systemctl stop {name}.service")
        except CommandError as error:
            if error.exit_code != 5:
                raise error

    def start_service(self, name: str, restart: bool = False):
        if restart:
            self.exec_command(f"sudo systemctl restart {name}.service")
        else:
            self.exec_command(f"sudo systemctl start {name}.service")
        self.exec_command(f"sudo systemctl enable {name}.service")

    def is_port_open(self, port: int):
        cmd = f"ss -tulnp sport = :{port} | wc -l"
        count, _ = self.exec_command(cmd)
        if int(count) > 1:
            return True
        return False
