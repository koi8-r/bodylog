import boto3 as aws
from botocore.exceptions import ClientError
import yaml


# language=YAML
example = """\
network:
    # empty values replaces with actual data from aws during execution
    vpc:
        id:
        name: docker-swarm-vpc  # only one vpc instance with this name
        cidr: '10.0.0.0/28'
        dhcp:
            id:
            domain: oz.internal
        gw:
            id:
"""

# yaml.load(example)

try:
    ec2 = aws.Session().resource('ec2')

    # gw = ec2.create_gw
    dhcp = ec2.create_dhcp_options(DhcpConfigurations=[{'Key': 'domain-name',
                                                        'Values': ['oz.internal']}])

    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/28')
    vpc.create_tags(Tags=[dict(Key='Name', Value='docker-swarm-vpc')])
    vpc.associate_dhcp_options(DhcpOptionsId=dhcp.id)
    # vpc.associate_gw

    print(yaml.safe_dump(dict(vpc_id=vpc.id,
                              dhcp_id=dhcp.id,
                              dhcp_domain=dhcp.domain)))
except ClientError as e:
    raise Exception('{}: "{}"'.format(*e.response['Error'].values()))
