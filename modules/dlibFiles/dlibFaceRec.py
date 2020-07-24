#!/usr/bin/env python

from scipy.spatial import distance
from imutils import face_utils
import numpy
import dlib
import copy
import cv2
import os

# collect list of faces[image] contained in project root dir
faceList = []
for filelist in os.listdir("Users/"):
    faceList.append("Users/" + filelist)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
faceRec = dlib.face_recognition_model_v1('./dlib_face_recognition_resnet_model_v1.dat')

cap = cv2.VideoCapture(0)           # use web camera as video source
cap.set(cv2.CAP_PROP_FPS, 2)        # set frame rate to lower

vbidiuk_user_set = []

while(True):
    ret, frame = cap.read()         # get frame from video
    origin = copy.copy(frame)       # copy original frame to origin variable
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert frame to gray

    rects = detector(gray, 0)       # find cordinates of rects with face on the frame
    for (i, rect) in enumerate(rects):
        shape = predictor(gray, rect)            # return image prediction <dlib.full_object_detection object ...>
        points = face_utils.shape_to_np(shape)   # return 68 facepoints cordinates on image

        for (x, y) in points: cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)    # draw each of 68 points
        face_descriptor1 = faceRec.compute_face_descriptor(origin, shape)      # return 128 paramentes of your face

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        for i in range(len(faceList)):
            Buffer = cv2.imread(faceList[i])

            rects = detector(Buffer, 0) # face cord on the image from folder
            for (i, rect) in enumerate(rects):
                Shape = predictor(Buffer, rect)  # return image prediction <dlib.full_object_detection object ...>
            face_descriptor2 = faceRec.compute_face_descriptor(Buffer, Shape)  # return 128 paramentes of face on the photo

            a = distance.euclidean(face_descriptor1, face_descriptor2)  # calculate distance of points between your face and photos
            if (a < 0.6):
                # cv2.imshow("Access allowed to: ", Buffer)
                print("Access allowed to: {}".format(faceList[i]))
                vbidiuk_user_set.append(list(face_descriptor2))
            else:
                print("Access not allowed!")

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

trend = numpy.array(vbidiuk_user_set)
print("Trend list varibles: {}".format(trend))

print("Mean value for vbidiuk user: {}".format(numpy.mean(trend, axis=0)))

cap.release()
cv2.destroyAllWindows()
