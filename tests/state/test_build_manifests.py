from kubeoven.state.build_manifests import build_network_manifest
from kubeoven.state import Manifest
from kubeoven.conf import ClusterConf
from unittest.mock import PropertyMock, patch 
import json
import yaml
import os

def test_build_network_manfiest():
    cluster = ClusterConf(
        kubernetes_version="v1.20.0",
        nodes=[{ # type: ignore
        'address': '10.0.0.1',
    }])
    dst = os.path.join(os.path.dirname(__file__), 'kube-flannel.yml')
    with patch.object(Manifest, 'path', new_callable=PropertyMock(return_value=dst)) as m:
        manifest = build_network_manifest(cluster)
        docs = list(yaml.safe_load_all(manifest.build(cluster)))
        assert len(docs) > 0
        daemon_set = next(doc for doc in docs if doc['kind'] == 'DaemonSet')
        spec = daemon_set['spec']['template']['spec']
        for container in spec['containers'] + spec['initContainers']:
            assert container['image'].startswith("rancher/")

def test_build_network_manifest_with_registry():
    cluster = ClusterConf(
        kubernetes_version="v1.20.0",
        nodes=[{ # type: ignore
        'address': '10.0.0.1',
        'role': ['registry']
    }])
    dst = os.path.join(os.path.dirname(__file__), 'kube-flannel.yml')
    with patch.object(Manifest, 'path', new_callable=PropertyMock(return_value=dst)) as m:
        manifest = build_network_manifest(cluster)
        docs = list(yaml.safe_load_all(manifest.build(cluster)))
        assert len(docs) > 0
        daemon_set = next(doc for doc in docs if doc['kind'] == 'DaemonSet')
        spec = daemon_set['spec']['template']['spec']
        for container in spec['containers'] + spec['initContainers']:
            assert container['image'].startswith(cluster.registry_uri())
        config_map = next(doc for doc in docs if doc['kind'] == 'ConfigMap')
        config = json.loads(config_map['data']['net-conf.json'])
        assert config['Network'] == cluster.cluster_cidr
        
            
            
            
            

