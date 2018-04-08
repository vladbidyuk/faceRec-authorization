from scipy.spatial import distance
from imutils import face_utils
import dlib
import copy
import cv2

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("Modules/dlibFiles/shape_predictor_68_face_landmarks.dat")
faceRec = dlib.face_recognition_model_v1('Modules/dlibFiles/dlib_face_recognition_resnet_model_v1.dat')

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    origin = copy.copy(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    rects = detector(gray, 0)

    for (i,rect) in enumerate(rects):
        shape = predictor(gray, rect)
        shape1 = face_utils.shape_to_np(shape)

        for (x, y) in shape1: cv2.circle(frame, (x,y), 2, (0,255,0), -1)
        face_descriptor1 = faceRec.compute_face_descriptor(origin, shape)

        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Buffer = cv2.imread("Users/user1.jpg")

        rects = detector(Buffer, 0)
        for (i, rect) in enumerate(rects):  Shape = predictor(Buffer, rect)
        face_descriptor2 = faceRec.compute_face_descriptor(Buffer, Shape)

        a = distance.euclidean(face_descriptor1, face_descriptor2)
        print("distance.euclidean = ", a)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):   break

cap.release()
cv2.destroyAllWindows()
