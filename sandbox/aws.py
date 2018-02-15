import boto3 as aws
import botocore as aws_core


sess = aws.Session(profile_name='default')
# ec2 = sess.client('ec2')  # client api
ec2 = sess.resource('ec2')  # resource api
for instance in ec2.instances.all():
    print(instance.state['Name'])

# https://docs.aws.amazon.com/cli/latest/reference/sqs/index.html
# https://boto3.readthedocs.io/en/latest/guide/sqs.html
# https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/Welcome.html
sqs = sess.resource('sqs')  # resource sqs
# aws sqs create-queue --queue-name test.fifo --attribute FifoQueue=true
queue = sqs.create_queue(QueueName='test', Attributes={'FifoQueue': True})
# aws sqs send-message --message-deduplication-id 128 --queue-url https://us-east-2.queue.amazonaws.com/495457580904/test.fifo --message-group-id main --message-body hello
