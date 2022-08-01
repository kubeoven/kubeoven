import openstack
import sys
import argparse
import yaml


def main():
    parser = argparse.ArgumentParser(description='create kubeoven config from openstack stack')
    parser.add_argument('stack', help='name of the created stack')
    args = parser.parse_args()

    client = openstack.connect()
    stack = client.get_stack(args.stack)
    if stack == None:
        sys.exit(f'stack "{args.stack}" not found')

    bastion_address = get_output(stack, 'bastion')
    controlplane_output = get_output(stack, 'controlplane')
    worker_output = get_output(stack, 'worker')

    controlplane = [{
        'user': 'ubuntu',
        'address': address,
        'role': ['controlplane', 'etcd', 'cache']
    } for address in controlplane_output]
    worker = [{
        'user': 'ubuntu',
        'address': address,
        'role': ['worker']
    } for address in worker_output]
    
    out = yaml.dump({
        'kubernetes_version': 'v1.20.0',
        'nodes': worker + controlplane,
        'bastion_host': {
            'address': bastion_address,
            'user': 'ubuntu'
        }
    })
    with open('cluster.yaml', 'w') as file:
        file.write(out)
    

def get_output(stack, key):
    for output in stack.outputs:
        if output['output_key'] == key:
            return output['output_value']
    sys.exit('stack output f"{key}" not found')

if __name__ == "__main__":
    main()


