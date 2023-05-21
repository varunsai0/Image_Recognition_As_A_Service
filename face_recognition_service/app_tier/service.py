import io
import base64
import literals
import subprocess
import PIL.Image as Image
#import  queue_handler as sqs_service
from web_tier.handlers import queue_handler as sqs_service
#from data_tier.handlers import s3_handler as s3_service
images_path='/home/ec2-user/app_tier/'
#input_s3_bucket='input-temp1'
#output_s3_bucket='output-temp1'

def initiate_service():
    get_imageid_from_sqs()

def get_imageid_from_sqs():
    images=receive_messages(literals.REQUEST_QUEUE_NAME,1,3,True)
    run_shell_command(images)

def receive_messages(queue_name,max_number,wait_time,to_delete=True):
    queue=sqs_service.get_queue_object(queue_name=queue_name)
    messages=queue.receive_messages(
        MessageAttributeNames=['All'],
        MaxNumberOfMessages=max_number,
        WaitTimeSeconds=wait_time,
    )
    image_ids={}
    print(messages)
    for message in messages:
        image_name=message.message_attributes['image_name']['StringValue']
        message_from_sqsqueue = message.message_attributes['encoded_image']['StringValue']
        byte_conversion=message_from_sqsqueue.encode('utf-8')
        decoded_output=base64.b64decode(byte_conversion)
        image_ids[image_name]=decoded_output
        if to_delete:
            message.delete()
    return image_ids

def run_shell_command(image_ids):
    if len(image_ids)>0:
        image_name = list(image_ids.keys())[0]
        img=Image.open(io.BytesIO(image_ids[image_name]))
        img.save(images_path+image_name)
        prediction=subprocess.check_output(['python3',images_path+'face_recognition.py',images_path+image_name])
        prediction_output=prediction.strip().decode('utf-8')
        upload_prediction_results(img,str(image_name),prediction_output)
    
def upload_prediction_results(image,image_name, result):
    message_attributes={
                    'image_name':{ 
                    'DataType': 'String',
                    'StringValue': image_name
                        },
                    'prediction':{ 
                    'DataType': 'String',
                    'StringValue': result
                        }
                }
    sqs_service.send_message_to_queue(literals.RESPONSE_QUEUE_NAME, image_name, message_attributes)
    # s3_service.upload_file_to_s3bucket(image, image_name, input_s3_bucket)
    # s3_service.upload_file_to_s3bucket(result, image_name, output_s3_bucket)