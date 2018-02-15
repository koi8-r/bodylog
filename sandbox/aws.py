import boto3 as aws
from botocore.exceptions import ClientError


def mk_attr(value):
    if isinstance(value, (str, int)):
        return dict(StringValue=str(value), DataType='String')
    else:
        raise ValueError('Cant make attribute from type {}'.format(type(value).__name__))


class Q(object):
    def __init__(self, sqs, name='test.fifo') -> None:
        super().__init__()
        self.sqs = sqs

        def mk():
            """$ aws sqs create-queue --queue-name <name>.fifo --attribute FifoQueue=true"""
            try:
                q = self.sqs.get_queue_by_name(QueueName=name)
                assert q.attributes['FifoQueue'], 'Conflict: not a FIFO queue "{}" already exists'.format(name)
            except ClientError as e:
                if type(e).__name__ == 'QueueDoesNotExist':
                    q = self.sqs.create_queue(QueueName=name, Attributes={'FifoQueue': 'true'})
                elif type(e).__name__ == 'QueueDeletedRecently':
                    from time import sleep
                    sleep(60)
                    return mk()
                else:
                    raise e

            return q

        self.q = mk()

    def send(self, message):
        # aws sqs send-message --message-deduplication-id <rand> \
        # --queue-url <url> --message-group-id <name> --message-body <text>
        self.q.send_message(MessageBody=message,
                            MessageAttributes={'UA': mk_attr('py3')},
                            MessageDeduplicationId='Z' * 128,
                            MessageGroupId='main')


sess = aws.Session(profile_name='default')
sqs = sess.resource('sqs')  # resource api sqs
q = Q(sqs)
q.send('Hello, World!')

print('\n'.join(_ for _ in (q.attributes['QueueArn'].split(':')[-1] for q in sqs.queues.all())))
