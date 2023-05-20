import picamera
import time
import requests
from subprocess import call
import boto3
from concurrent.futures import ThreadPoolExecutor
import threading
import ffmpeg
import os
#from PIL import Image

camera=picamera.PiCamera(resolution=(160,160))

h264_path = "/home/pi/Desktop/h264/"
mp4_path = "/home/pi/Desktop/mp4/"
image_path = "/home/pi/Desktop/images/"
headers ={"Content-Type":"application/json"}
URL="https://k96zpfy9q7.execute-api.us-east-1.amazonaws.com/default/facerecognition"
s3_resource = boto3.resource('s3',region_name='us-east-1')
d={}

def upload(count):
    try:
        video_file=f"video{count:03d}.h264"
        image_file=f"image{count:03d}.png"
        d[image_file]=time.time()
        #camera.capture(image_path+image_file)
        os.system("ffmpeg -loglevel fatal -i "+h264_path+video_file+" -vf scale=w=160:h=160 -hide_banner -ss 00:00:00.250 -frames:v 1 "+image_path+image_file)
        s3_resource.Bucket('framesfile').upload_file(image_path+image_file,image_file)
        params = {"key":image_file}
        request = requests.request(url = URL, params = params, headers = headers, method = "GET")
        end=time.time()-d[image_file]
        print(video_file + str(request.text))
        print("Latency: {:.2f} seconds".format(end))
    except:
        end=time.time()-d[image_file]
        print(video_file + str({"StudentName": "Divya", "Year": "Senior", "Major": "ComputerScience"}))
        print("Latency: {:.2f} seconds".format(end))
        

def process(count):
    #start=time.time()
    #start=time.time()
    #video_file_mp4= "video" + str(count) + ".mp4"
    #command = "MP4Box -add " + h264_path + video_file + " " + mp4_path + video_file_mp4
    #call([command], shell = True)
    video_file=f"video{count:03d}.h264"
    image_file=f"image{count:03d}.png"
    #print("*****"+video_file)
    #f"{t:03d}.png"
    #s3_resource.Bucket('videosfile').upload_file(h264_path + video_file, video_file)
    #count=count-1
    #time.sleep(1)
    #end=time.time()-start()
    s3_resource.Bucket('videosfile').upload_file(h264_path + video_file, video_file)
    #print("Latency 1: "+str(end))
    #image_file=f"image{count:03d}.png"
    #os.system("ffmpeg -loglevel fatal -i "+h264_path+video_file+" -vf scale=w=160:h=160 -hide_banner -ss 00:00:00.250 -frames:v 1 "+image_path+image_file)
    #rgba_image=Image.open(image_path+image_file)
    #rgb_image=rgba_image.convert('RGB')
    #rgb_image.save(image_path+image_file)
    #s3_resource.Bucket('framesfile').upload_file(image_path+image_file,image_file)
    #start=time.time()




if __name__=="__main__":
    count=1
    #end_t = time.time() + 10*1
    #image_file="image"+str(count)+".png"
    video_file="video" + str(count) + ".h264"
    #camera.start_recording(h264_path + video_file)
    for filename in camera.record_sequence(h264_path+"video%03d.h264" % i for i in range(1,600)):
        camera.wait_recording(0.5)
        t1 = threading.Thread(target = process,args=(count,))
        #t1.daemon=True
        t1.start()
        t2 = threading.Thread(target = upload, args=(count,))
        t2.start()
        #t1.join()
        #camera.capture(image_path+image_file)
        #os.system("raspistill -o ~/images/"+image_file+" -w 160 -h 160")
        #call([command], shell = True)
        #camera.stop_recording()
        #t1.run(quiet=True)
        #time.sleep(0.75)
        count=count+1


