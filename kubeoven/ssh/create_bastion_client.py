from typing import Optional
from paramiko import AutoAddPolicy, SSHClient
from kubeoven.conf import  BastionConf
from kubeoven.common.di import provide

def create_bastion_client(conf: BastionConf) -> SSHClient:
    client = SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(conf.address, conf.port)
    return client
    
def provide_bastion_client(conf: Optional[BastionConf]):
    if conf is None:
        return
    client = create_bastion_client(conf)
    provide(client, 'bastion')

