import yaml


with open('Moby AWS region to AMI.yml', 'rut') as fh:
    print(yaml.safe_load(fh)['map']['us-east-2'])
