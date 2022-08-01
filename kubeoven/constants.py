import os

ETCD_CLIENT_PORT = 2379

ROOT_DIR = os.getenv('APPDIR', os.path.dirname(__file__))

KUBEOVEN_DIR = os.path.join(os.getcwd(), '.kubeoven')

IMAGES_DIR = os.path.join(KUBEOVEN_DIR, 'images')

TEMPLATES_DIR = os.path.join(ROOT_DIR, 'templates')

CRANE_CLI = os.path.join(KUBEOVEN_DIR, 'bin', 'crane')

SUPPORTED_K8S_VERSIONS = [
    'v1.20.0',
    'v1.19.0'
    'v1.19.11',
    'v1.22.0',
    'v1.22.4'
]

K8S_GCR_REGISTRY = "k8s.gcr.io"