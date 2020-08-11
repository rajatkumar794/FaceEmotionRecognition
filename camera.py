import cv2
from model import FacialExpressionModel
import numpy as np

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()
        #print(fr)
        fr = cv2.flip(fr, 1)
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            fc = gray_fr[y:y+h, x:x+w]

            roi = cv2.resize(fc, (48, 48))
            pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
            #fr = cv2.resize(fr, (640, 480))
            cv2.putText(fr, pred, (x, y), font, 1, (0, 0, 255), 2)
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
            fr=cv2.resize(fr,(640,480),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        _, jpeg = cv2.imencode('.jpg', fr)
        return jpeg.tobytes()