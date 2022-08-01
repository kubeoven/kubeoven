# Kubeoven

Deploy production ready kubernetes cluster anywhere

## Quick start

Create a cluster.yaml with your server address
```yaml
# cluster.yaml
nodes:
    - address: 1.2.3.4
      user: ubuntu
      role:
        - etcd
        - controlplane
        - worker
```

Exec following command from same directory

```bash
kubeoven deploy
```

## Documentation

Documentation is in the `/docs` directory