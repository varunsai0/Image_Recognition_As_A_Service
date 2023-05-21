from logging import exception
import boto3
from botocore.exceptions import ClientError


s3_resource = boto3.resource('s3', aws_access_key_id='AKIAVAVQDZEI6G4T4NUP',
         aws_secret_access_key= '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', region_name = 'us-east-1')
s3_client = boto3.client('s3',aws_access_key_id='AKIAVAVQDZEI6G4T4NUP',
         aws_secret_access_key= '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', region_name = 'us-east-1')


def upload_results_to_s3bucket(prediction, s3bucket_name, input_image):
    try:
        input_image=input_image[:-4]
        s3_client.put_object(Bucket=s3bucket_name, Key=input_image, Body=prediction)
        print("------ prediction uploaded to s3")
    except ClientError as ex:
        print(ex)


def upload_image_to_s3bucket(file, s3bucket_name, file_name):
    try:
        acl="public-read"
        s3_client.upload_file(file, s3bucket_name, file_name)
        print("------ input image uploaded to s3")
    except ClientError as ex:
        print(ex)

