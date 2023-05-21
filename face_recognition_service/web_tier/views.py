from django.shortcuts import render
from web_tier.handlers import queue_handler as sqs_service
from web_tier import literals
#import literals
import base64
import time
from django.template.loader import render_to_string
from werkzeug.utils import secure_filename
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class get_requests:
    request_response_directory = {}   

@csrf_exempt
def run_app_tier(request):
    if request.method == 'POST':
        images = request.FILES.getlist('uploded_images')
        image = images[0]
        image_name = image.name
        

        all_requests = get_requests()
        print("dictionary" + str(all_requests.request_response_directory))
        
        encoded_image = base64.b64encode(image.file.read())
        encoded_string_image = encoded_image.decode('utf-8')

        message_attributes = {
            'image_name':{ 
                'DataType': 'String',
                'StringValue': image_name
                },
            'encoded_image':{ 
            'DataType': 'String',
            'StringValue': encoded_string_image
            }
        }

        sqs_service.send_message_to_queue(literals.REQUEST_QUEUE_NAME, encoded_string_image, message_attributes)

        all_requests.request_response_directory[image_name] = ''

        time.sleep(100)

        print("before" + str(len(all_requests.request_response_directory)))

        result = sqs_service.process_messages_from_response_queue(literals.RESPONSE_QUEUE_NAME,all_requests, image_name)

        print("çç" + str(len(result.request_response_directory)))

        print(image_name + "---" + str(result.request_response_directory[image_name]))
        return HttpResponse(str(result.request_response_directory[image_name]))
    else:
        context = {}
        return render(request, "face_recognition.html", context)