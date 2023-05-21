import imp
import boto3
#import literals
from web_tier import literals
import time
from botocore.exceptions import ClientError

sqs_resource = boto3.resource('sqs', aws_access_key_id = literals.ACCESS_KEY, aws_secret_access_key = literals.SECRET_ACCESS_KEY, region_name = literals.REGION)
sqs_client = boto3.client('sqs', aws_access_key_id = literals.ACCESS_KEY, aws_secret_access_key = literals.SECRET_ACCESS_KEY, region_name = literals.REGION)

def get_queue_object(queue_name):
    try:       
        queue_obj = sqs_resource.get_queue_by_name(QueueName = queue_name)
        return queue_obj
    except ClientError as ex:
        print(ex)

def send_message_to_queue(queue_name, message_body, message_attributes = None):
    try:
        queue = get_queue_object(queue_name)
        if not message_attributes:
            message_attributes = {}
        queue.send_message(MessageBody = message_body, MessageAttributes = message_attributes)
    except ClientError as ex:
        print(ex)

def get_number_of_messages_in_queue(queue_name):
    try:
        response=sqs_client.get_queue_attributes(
            QueueUrl=get_queue_object(queue_name).url,
            AttributeNames=['ApproximateNumberOfMessages']
        )
        return int(response['Attributes']['ApproximateNumberOfMessages'])
    except ClientError as ex:
        print(ex)

def get_messages_from_queue(queue_name, max_number_of_messages, wait_time_seconds, delete_message = True):
    try:
        queue = get_queue_object(queue_name)
        messages = queue.receive_messages(
            MessageAttributeNames=['All'],
            MaxNumberOfMessages = max_number_of_messages,
            WaitTimeSeconds = wait_time_seconds
        )
        if delete_message:
            for message in messages:
                message.delete()
    except ClientError as ex:
        print(ex)
    else:
        return messages

def process_messages_from_response_queue(queue_name, uploaded_images, image_name ):
    #uploaded_images is a dictionary not a set
    if image_name in uploaded_images.request_response_directory.keys():
        while(not uploaded_images.request_response_directory[image_name]):
            try:   
                print("trying to get message")    
                response_messages = get_messages_from_queue(queue_name, 1, 1, True)
                for message in response_messages:
                    print("trying to get single message")
                    
                    image_name_from_response = message.message_attributes["image_name"]['StringValue']
                    prediction = message.message_attributes["prediction"]['StringValue']
                    print(image_name_from_response + "---" + prediction) 
                    uploaded_images.request_response_directory[image_name_from_response] = prediction 
            except ClientError as ex:
                print(ex)
        return uploaded_images
