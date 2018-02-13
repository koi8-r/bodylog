Documentation: |
    http://docs.amazonaws.cn/en_us/cli/latest/index.html
    https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Subnets.html
    https://gist.github.com/joshpadilla/566362
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html
    https://stackoverflow.com/questions/23044317/aws-vpc-create-subnet-in-with-different-zone
https://www.linuxsecrets.com/2058-aws-ec2-vpc-cli
http://asyoulook.com/computers%20&%20internet/amazon-web-services-aws-cli-create-default-vpc/724177
    https://www.linuxsecrets.com/2058-aws-ec2-vpc-cli
    https://editions-us-east-1.s3.amazonaws.com/aws/stable/Docker.tmpl
    https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpc-subnets-commands-example.html
    http://blmte.com/professional/5962266_aws-cli-create-default-vpc
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html

Examples: https://github.com/aws/aws-cli/tree/develop/awscli/examples/ec2
Show info about AMI: >
    aws ec2 describe-images --image-id ami-2eac874b --query 'Images[0].Name'
    aws ec2 describe-images --query 'Images[?starts_with(Name,`Moby Linux`) == `true`]'
Regions list: >
    aws ec2 describe-regions --query 'Regions[].{Name:RegionName}' --output text
List first available zone: >
    aws ec2 describe-availability-zones --query
    'AvailabilityZones[?State == `available`]
     | [?RegionName == `us-east-2`]
     | [0].ZoneName'
    --output text
Network:
  GW: aws ec2 describe-internet-gateways
  IF: aws ec2 describe-network-interfaces
  Net: |
      aws ec2 create-default-subnet --availability-zone us-east-2a
      aws ec2 create-vpc --cidr-block 192.168.10.0/24
  Allocate EC2-VPC address: |
      aws ec2 allocate-address --domain vpc
      aws ec2 release-address help
  Route: '...'
Docker for AWS instance user data: >
    aws ec2 describe-instance-attribute --attribute userData --output text
    --query "UserData.Value" --instance-id i-00d6dcd630347ed43
    | base64 -d | vim -

