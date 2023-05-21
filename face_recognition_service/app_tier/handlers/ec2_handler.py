#from app_tier import service
from botocore.exceptions import ClientError
import boto3
#from app_tier import literals
#import literals

# ec2_resource = boto3.resource('ec2', aws_access_key_id = literals.ACCESS_KEY, aws_secret_access_key = literals.SECRET_ACCESS_KEY, region_name = literals.REGION)
# ec2_client = boto3.client('ec2', aws_access_key_id = literals.ACCESS_KEY, aws_secret_access_key = literals.SECRET_ACCESS_KEY, region_name = literals.REGION)

ec2_resource = boto3.resource('ec2', aws_access_key_id='AKIAVAVQDZEI6G4T4NUP',
         aws_secret_access_key= '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',region_name='us-east-1')
ec2_client = boto3.client('ec2', aws_access_key_id='AKIAVAVQDZEI6G4T4NUP',
         aws_secret_access_key= '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',region_name='us-east-1')

def create_ec2_instance(instance_name,image_id, instance_type, key_name, security_groups):
    try:
        user_data_init_app = '''#!/bin/bash
        python3 /root/app_tier/poller.py'''

        instance_params = {
                'ImageId': image_id, 'InstanceType': instance_type, 'KeyName': key_name,
                'UserData': user_data_init_app
        }
        if security_groups is not None:
                instance_params['SecurityGroups'] = security_groups

        instance=ec2_resource.create_instances(**instance_params,MinCount=1,MaxCount=1)
        #poller.initiate_service()
        instance_id= instance[0].id
        return instance_id
    except ClientError as ex:
        print(ex)

def terminate_ec2_instance(instance_id):
    try:
        ec2_resource.instances.filter(InstanceIds = instance_id).terminate()
    except ClientError as ex:
        print(ex)

def get_count_of_instances():
    try:
        image_id=['ami-043f85840dd795ce9']
        instances_count=0
        running_instances = ec2_client.describe_instances(Filters=[
                #{'Name':'image-id', 'Values': image_id},
                {'Name':'instance-state-name', 'Values':['running' , 'pending']}]
        )
        instances_count = len(running_instances['Reservations'])
        return instances_count
    except ClientError as ex:
        print(ex)

print(get_count_of_instances())