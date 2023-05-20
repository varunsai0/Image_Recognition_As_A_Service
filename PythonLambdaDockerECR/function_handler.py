from PIL import Image

from matplotlib.pyplot import table


try:

    import json
    import boto3
    import json
    import os
    import eval_face_recognition
    print("All imports ok ...")
except Exception as e:
    print("Error Imports : {} ".format(e))

s3 = boto3.resource('s3', region_name = "us-east-1")
dynamodb=boto3.resource('dynamodb', region_name = "us-east-1")
# image_path="images/"
video_path="/tmp/"
bucket = "framesfile"
table=dynamodb.Table("StudentAcademicInfo")


def lambda_handler(event, context):

    
    # key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    key=event['queryStringParameters']['key']
    try:
        # print(str(bucket)+"   key   "+str(key)+"   path   "+video_path+str(key))
        s3.Bucket(bucket).download_file(key,video_path+key)
        # image_path=key[:-4]
        # s3.Bucket(str(bucket)).upload_file(video_path+str(key),"testing.mp4")
        # os.makedirs(video_path+image_path)
        # os.system("ffmpeg -i "+video_path+key+" -ss 00:00:00.250 -frames:v 1 "+video_path+image_path+".png")
        # image_name=urllib.parse.unquote_plus(event['key'], encoding='utf-8')
        print("Entered Lambda function"+str(event))
        rgba_image = Image.open(video_path+key)
        rgb_image = rgba_image.convert('RGB')
        rgb_image.save(video_path+key)
        # file_name=event['headers']['file-name']
        # file_content=base64.b64decode(event['body'])
        # image_name=event['key']
        print("Image taken from api")
        response=eval_face_recognition.testing1(video_path+key)
        print("face recognition completed")
        result=table.get_item(
                Key={
                    'StudentName':response
                }
            )
        print("Dynamo DB result is taken"+str(result["Item"]))    
        response_object={}
        response_object['statusCode']=200
        response_object['headers'] = {}
        response_object['headers']['Content-Type']='application/json'
        response_object['body']=json.dumps(result["Item"])
        print("Added to response object")
        # images=load_images_from_folder(video_path+image_path,str(key))
        # for i in images:
            # print(i)
        # print("CONTENT TYPE: " + response['ContentType'])
        # return response['ContentType']
    except Exception as e:
        print(e)
        # print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
    print("Hello AWS!")
    print(response_object["body"])
    print("event = {}".format(event))
    return response_object


def load_images_from_folder(folder,key):
    images = []
    count=0
    f=open(str(key)[:-4]+".txt",'a')
    for filename in os.listdir(folder):
        if filename.endswith('.png'):
            # s3.Bucket('inputtemp').upload_file(folder+filename,filename)
            # response=subprocess.check_output(['python3',folder+'eval_face_recognition.py',"--img_path",folder+"image-015.png"])
            response=eval_face_recognition.testing1(folder+filename)
            result=table.get_item(
                Key={
                    'StudentName':response
                }
            )
            f.write(str(result["Item"])+"\n")
            images.append(response)
            print("Result"+str(result["Item"])+"  \n Response"+response)
    return images