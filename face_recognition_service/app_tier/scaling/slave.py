
import handlers.ec2_handler as ec2_service
from web_tier.handlers import queue_handler as sqs_service
from app_tier import service
# import ec2_handler as ec2_service
# import queue_handler as sqs_service
# import service

from ec2_metadata import ec2_metadata
from botocore.exceptions import ClientError

def slave_scaling(sqs_queue):
    try:
        ec2_resource = ec2_service.ec2_resource
        while True:
            number_of_messages = sqs_service.get_number_of_messages_in_queue(sqs_queue)
            if number_of_messages > 0:
                service.initiate_service()
            else:
                instance_id = ec2_metadata.instance_id
                ec2_resource.Instance(instance_id).terminate()
    except ClientError as ex:
        print(ex)

slave_scaling('REQUEST_QUEUE')
