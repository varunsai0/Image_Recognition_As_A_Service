#from app_tier.handlers import literals
from web_tier.handlers import queue_handler as sqs_service
import handlers.ec2_handler as ec2_service

max_number_of_instances=20
slaves_capacity = max_number_of_instances - 1
def create_instances_as_per_sqsrequests(sqs_queue):
    slave_ami = "ami-043f85840dd795ce9"
    instance_name = "app-instance1"
    while True:
        number_of_messages = sqs_service.get_number_of_messages_in_queue(sqs_queue)
        if number_of_messages > 0 and ec2_service.get_count_of_instances() < slaves_capacity:
            ec2_service.create_ec2_instance(instance_name,slave_ami,"t2.micro","TestingPurpose",["launch-wizard-2"])

create_instances_as_per_sqsrequests('REQUEST_QUEUE')

