#!/usr/bin/env python

from imutils import face_utils
import argparse
import numpy
import dlib
import copy
import cv2
import os

# ======================================================================== #
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", required = True, help = "mode for application")
args = vars(parser.parse_args())
# ======================================================================== #


def handleUsersFile(mode, data, fileLoc="users/allowed_users.csv"):
    if (mode == "read"):
        return(numpy.loadtxt(fileLoc, delimiter=','))
    elif (mode == "write"):
        numpy.savetxt(fileLoc, numpy.asarray(data), delimiter=',')
        print("{}: File written successfully".format(handleUsersFile.__name__))
    else:
        print("{}: Unknown mode!".format(handleUsersFile.__name__))


def configuration_mode(user_data_array):
    print("configuration mode!")
    print("Mean value for user: {}".format(numpy.mean(numpy.array(user_data_array), axis=0)))
    pass


def monitoring_mode():
    print("monitoring mode!")
    pass


def main():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("Modules/dlibFiles/shape_predictor_68_face_landmarks.dat")
    faceRec = dlib.face_recognition_model_v1('Modules/dlibFiles/dlib_face_recognition_resnet_model_v1.dat')

    cap = cv2.VideoCapture(0)           # use web camera as video source
    cap.set(cv2.CAP_PROP_FPS, 2)       # set frame rate to lower

    while(True):
        ret, frame = cap.read()                         # get frame from video
        origin = copy.copy(frame)                       # copy original frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert frame to gray



        rects = detector(gray, 0)                       # find cordinates of rects with face on the frame
        for (i, rect) in enumerate(rects):
            shape = predictor(gray, rect)               # return image prediction <dlib.full_object_detection object ...>
            points = face_utils.shape_to_np(shape)      # return 68 facepoints cordinates on image

            for (x, y) in points: cv2.circle(frame, (x, y), 2, (0, 255, 0), -1)    # draw each of 68 points
            face_descriptor = faceRec.compute_face_descriptor(origin, shape)       # return 128 paramentes of your face

            if (args['mode'] == "config"):
                user_data_array = []
                user_data_array.append(list(face_descriptor))
                configuration_mode(user_data_array)


            elif (args['mode'] == "monitoring"):
                monitoring_mode()


            else:
                print("Unknown mode!")
                exit(1)

        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
