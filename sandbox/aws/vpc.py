import boto3 as aws
from botocore.exceptions import ClientError
import yaml


# language=YAML
example = """\
network:
    vpc:
        id:
        instances:
        gw:
        if:
        route:
        fw:
        net:

    dhcp:
        id:
        domain:
"""


class Networking(object):
    def __init__(self):
        self.vpc_id = None
        self.dhcp_id = None
        self.domain = None


res = Networking()


try:
    ec2 = aws.Session().resource('ec2')

    # gw = ec2.create_gw
    dhcp = ec2.create_dhcp_options(DhcpConfigurations=[{'Key': 'domain-name',
                                                        'Values': ['oz.internal']}])

    vpc = ec2.create_vpc(CidrBlock='10.0.0.0/28')
    vpc.associate_dhcp_options(DhcpOptionsId=dhcp.id)
    # vpc.associate_gw

    res.vpc_id = vpc.id
    res.dhcp_id, res.domain = dhcp.id, 'oz.internal'
    print(yaml.safe_dump(res.__dict__))
except ClientError as e:
    raise Exception('{}: "{}"'.format(*e.response['Error'].values()))
