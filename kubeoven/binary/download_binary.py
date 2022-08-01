import os
import hashlib
from urllib import request
from multiprocessing import Pool
from kubeoven import ssh, log, conf
from typing import Union
from .binary import Binary
from .binaries import get_binaries


def download_binaries(cluster: conf.ClusterConf):
    bins = get_binaries(cluster)
    with Pool(1) as p:
        p.map(download_binary, bins)


def download_binary(bin: Binary):
    path = bin.path()
    if os.path.isfile(path) and compare_sha256(path, bin.sha256):
        log.info(f"using cached {bin.filename} {bin.version}")
        return bin
    os.makedirs(os.path.dirname(path), 0o775, exist_ok=True)
    log.info(f"downloading {bin.filename} {bin.version}")
    request.urlretrieve(bin.url, path)
    return bin


def copy_binary_to_node(
    bin: Binary, dest: str, cache_server: Union[str, None], client: ssh.NodeClient
):
    if cache_server:
        download_binary_to_node(bin, dest, cache_server, client)
    else:
        upload_binary_to_node(bin, dest, client)


def upload_binary_to_node(bin: Binary, dest: str, client: ssh.NodeClient):
    try:
        is_binary_present_on_node(bin, dest, client)
    except FileNotFoundError:
        log.info(f"upload file {bin.filename}")
        client.ensure_dirs(os.path.dirname(dest))
        client.sftp.put(bin.path(), dest)


def download_binary_to_node(bin: Binary, dest: str, cache_server: str, client: ssh.NodeClient):
    try:
        is_binary_present_on_node(bin, dest, client)
    except FileNotFoundError:
        log.info(f"download file {bin.filename}")
        url = f"http://{cache_server}:8383{bin.path('/')}"
        client.exec_command(f"sudo curl -o {dest} {url}")

def is_binary_present_on_node(bin: Binary, dest: str, client: ssh.NodeClient):
    client.sftp.stat(dest)
    out, _ = client.exec_command(f"sha256sum {dest}")
    if not out.startswith(bin.sha256):
        raise FileNotFoundError(dest)

def compare_sha256(filename: str, hash: str) -> bool:
    sha = hashlib.sha256()
    size = 4096 * 4
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(size), b""):
            sha.update(chunk)
    calc = sha.hexdigest()
    return calc == hash


# https://github.com/google/go-containerregistry/releases/download/v0.11.0/go-containerregistry_Darwin_x86_64.tar.gz
# https://github.com/google/go-containerregistry/releases/download/0.11.0/go-containerregistry_Darwin_x86_64.tar.gz