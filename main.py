# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# import the opencv library
import csv

import boto3
import cv2

access_key_id = None
secret_key_id = None
# Setup
# font
font = cv2.FONT_HERSHEY_SIMPLEX

# org
org = (50, 50)

# fontScale
fontScale = 0.5

# Blue color in BGR
color = (255, 0, 0)

# Line thickness of 2 px
thickness = 1

scale_factor = .15
green = (0, 255, 0)
red = (0, 0, 255)
frame_thickness = 2


def get_cred():
    """read csv and get access and secret key"""
    global access_key_id
    global secret_key_id
    with open("shijo@nuventure.in_accessKeys.csv", 'r') as input:
        next(input)
        reader = csv.reader(input)

        for line in reader:
            access_key_id = line[0]
            secret_key_id = line[1]


get_cred()
region = "eu-west-1"
rekognise = boto3.client("rekognition", aws_access_key_id=access_key_id,
                         aws_secret_access_key=secret_key_id, region_name=region)

# define a video capture object
webcam = cv2.VideoCapture(0)

while True:

    # Capture the video frame
    # by frame
    ret, frame = webcam.read()
    height, width, channels = frame.shape

    # Convert frame to jpg
    small = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))
    ret, buf = cv2.imencode('.jpg', small)

    # Detect faces in jpg
    faces = rekognise.detect_faces(Image={'Bytes': buf.tobytes()}, Attributes=['ALL'])

    # Draw rectangle around faces
    for face in faces['FaceDetails']:
        smile = face['Smile']['Value']
        gender = str(face['Gender']['Value'])
        age = "(" + str(face['AgeRange']["Low"]) + "-" + str(face['AgeRange']['High']) + ")"
        cv2.putText(frame, gender + age,
                    (int(face['BoundingBox']['Left'] * width), int(face['BoundingBox']['Top'] * height - 10)),
                    font, fontScale, color, thickness, cv2.LINE_AA
                    )
        cv2.rectangle(frame,
                      (int(face['BoundingBox']['Left'] * width),
                       int(face['BoundingBox']['Top'] * height)),
                      (int((face['BoundingBox']['Left'] + face['BoundingBox']['Width']) * width),
                       int((face['BoundingBox']['Top'] + face['BoundingBox']['Height']) * height)),
                      green if smile else red, frame_thickness)

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# After the loop release the cap object
webcam.release()
# Destroy all the windows
cv2.destroyAllWindows()
