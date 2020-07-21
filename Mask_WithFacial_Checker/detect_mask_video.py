from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import cv2
import os
import numpy as np
import argparse
import imutils
import time
import dlib

def mouth_aspect_ratio(mouth):  #mouth aspect ratio
    A = dist.euclidean(mouth[2], mouth[10]) 
    B = dist.euclidean(mouth[4], mouth[8]) 
    C = dist.euclidean(mouth[0], mouth[6]) 
    mar = (A + B) / (2.0 * C)
    return mar

def nose_aspect_ratio(nose):
    A=dist.euclidean(nose[0],nose[6])
    B=dist.euclidean(nose[4],nose[7])  
    nar = A/B
    return nar

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

def detect_and_predict_mask(frame, faceNet, maskNet):
    (h,w)=frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame,1.0,(300,300),(104.0,177.0,123.0))
    faceNet.setInput(blob)
    detections = faceNet.forward()
    faces=[]
    locs=[]
    preds=[]
    for i in range(0, detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence > args["confidence"]:
            box = detections[0,0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w-1, endX), min(h-1, endY))
            face = frame[startY:endY, startX:endX]
            face = cv2.cvtColor(face,cv2.COLOR_BGR2RGB)
            face = cv2.resize(face,(224,224))
            face = img_to_array(face)
            face = preprocess_input(face)
            face = np.expand_dims(face, axis=0)
            faces.append(face)
            locs.append((startX,startY,endX,endY))
    if (len(faces) > 0):
        preds = maskNet.predict(faces)
    return (locs,preds)
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", type=str,default="face_detector",help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,default="mask_detector1.model",help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
print("[INFO] loading face detector model...")
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],"res10_300x300_ssd_iter_140000.caffemodel"])
faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)

# load the face mask detector model from disk
print("[INFO] loading face mask detector model...")
maskNet = load_model(args["model"])

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
frame_width = 640
frame_height =360
(mStart, mEnd) = (49, 68)
(nStart, nEnd) = (28,36)
# loop over the frames from the video stream
while True:
    frame = vs.read()
    frame=imutils.resize(frame, width=400)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)
    (locs, preds) = detect_and_predict_mask(frame, faceNet, maskNet)
    print(preds)
    for(box,pred) in zip(locs,preds):
        (startX,startY,endX,endY) = box
        (mask, withoutMask) = pred
        
        if(mask>withoutMask):
            label = "Mask"
        else:
            label = " No Mask"
        if (label == "Mask"):
            color = (0, 255, 0)
        else:
            color = (0, 0, 255)
        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
        cv2.putText(frame, label, (startX, startY - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)
            mouth = shape[mStart:mEnd]
            nose  = shape[nStart: nEnd]
            mouthMAR = mouth_aspect_ratio(mouth)
            noseMAR = nose_aspect_ratio(nose)
            mar = mouthMAR
            nar = noseMAR

            mouthHull = cv2.convexHull(mouth)
            noseHull  = cv2.convexHull (nose)

            cv2.drawContours(frame, [mouthHull], -1, (255, 0, 0), 1)
            #cv2.putText(frame, "MAR: {:.2f}".format(mar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.drawContours(frame, [noseHull], -1, (255, 0, 0), 1)
            #cv2.putText(frame, "MAR: {:.2f}".format(nar), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255),
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(5) & 0xFF
	# show the output frame
    if key == ord("q"):
        break
    if ( withoutMask > 2*mask):
        mail = 1
    else:
        mail = 0
# do a bit of cleanup
#from firebase import firebase

#firebase = firebase.FirebaseApplication('https://mask-detection-283520.firebaseio.com/', None)
print(withoutMask)
print('*',mask)
#if (mail==1):
 #   firebase.put('/mask-detection-283520/User-S2','Status',True)
#else:
 #   firebase.put('/mask-detection-283520/User-S2','Status',False)
cv2.destroyAllWindows()
vs.stop()



































