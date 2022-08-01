
def etcd_peer_url(ip:str):
    return f"https://{ip}:2380"

def etcd_client_url(ip:str):
    return f"https://{ip}:2379"
