from kubeoven import ssh, binary
from kubeoven.state import FullState
from multiprocessing import Pool, cpu_count

KUBEOVEN_CACHE_ROOT = '/var/cache/kubeoven'

def upload_cache(full_state: FullState, address: str):
    args = []
    for bin in binary.get_binaries(full_state.config):
        args.append([bin, full_state, address])
    with Pool(processes=cpu_count()) as pool:
        pool.starmap(upload_cached_binary, args)
    

def upload_cached_binary(bin: binary.Binary, full_state: FullState, address: str):
    dst = bin.path(KUBEOVEN_CACHE_ROOT)
    with ssh.create_node_client(full_state, address) as client:
        binary.upload_binary_to_node(bin, dst, client)

