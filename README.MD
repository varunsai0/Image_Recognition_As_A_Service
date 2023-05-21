


How to Run:

1.	Download Docker from the link below and install.
https://docs.docker.com/get-docker/
2.	Go to the project directory in the terminal where it is extracted and run the below command:
“docker build -t docker_container .”
3.	Inorder to test the code in local machine, run the docker using the below command:
“docker run -p 9000:8080 docker_container”
4.	To test the docker container’s invocation and output we need to run the below command terminal:
“curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d {"queryStringParameters":{"key":"frame.png"}}”
5.	This should give the output of the Student Academic Information of the student present in the image.
6.	In the Raspberry PI run the below commands in the terminal to install the dependencies related to python file:
“Pip install boto3”
“Pip install ffmpeg-python”

7. Then copy the file “RaspberryPiVideoProcessing.py” to RaspberryPI. Go to the directory where the file is present and run the below command in the terminal
“Python3 RaspberryPiVideoProcessing.py”
8.  Keep the face in front of the camera to predict the face with a raspberry pi camera by machine learning module. 
9.  The prediction person academic details from DynamoDB along with the latency gets displayed on the Raspberry Pi. 

