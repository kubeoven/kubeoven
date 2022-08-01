from kubeoven.state.build_manifests import build_network_manifest
from kubeoven.conf import ClusterConf

def test_image_ref():
    cluster = ClusterConf(
        kubernetes_version="v1.20.0",
        nodes=[{
        'address': '10.0.0.1',
        'roles': ['registry']
    }])
    manifest = build_network_manifest(cluster)
    out = manifest.get()
    print(out)
    # out = render_string("Hi, {{ data.get('users').names.first }}", data={})
    # print(out)
    # exp = parse("users[*].name")
    # print(exp.update({'users': [{'name': 'abc'}]}, 'nauman'))
    # image = ImageRef.of("ubuntu:latest")
    # assert image.name == "ubuntu:latest"
    # image = ImageRef.of("quay.io/jetstack/cert-manager-cainjector")
    # assert image.name == "jetstack/cert-manager-cainjector"
    # image = ImageRef.of("nginx/nginx")
    # assert image.name == "nginx/nginx"
