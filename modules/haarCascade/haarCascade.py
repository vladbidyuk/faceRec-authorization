#!/usr/bin/env python

import numpy
import cv2
import os

face_cascade = cv2.CascadeClassifier('Modules/haarCascade/haarcascade_frontalface_default.xml')
#face_cascade = cv2.CascadeClassifier('Modules/haarCascade/haarcascade_frontalface_alt_tree.xml')

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()

    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,0,255), 2)


    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
