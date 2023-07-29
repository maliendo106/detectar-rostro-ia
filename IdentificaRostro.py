import cv2
import face_recognition
import numpy as np
import base64
import json
import re
import time
import sys


matriz = np.loadtxt("./perfil.txt")

cap=cv2.VideoCapture(0)
global start_time
start_time = time.time()

while True:
    ret, frame=cap.read()
    if ret == False:
        break

    frame=cv2.flip(frame,1)
    faces_loc=face_recognition.face_locations(frame)
    for fl in faces_loc:
        model=face_recognition.face_encodings(frame, known_face_locations=[fl])
        result=False
        for f in model:
            result = result or True in face_recognition.compare_faces([matriz],f)
        quien="Desconocid@"
        if result:
            cap.release()
            cv2.destroyAllWindows()
            print(1)

        cv2.rectangle(frame, (fl[3], fl[2]), (fl[1], fl[2]+30), (50,50,255), -1 )
        cv2.rectangle(frame, (fl[3], fl[0]), (fl[1], fl[2]), (50,50,255), 2 )
        cv2.putText(frame, quien , (fl[3], fl[2]+20),2,0.7,(255,255,255), 1)

    cv2.imshow('video', frame)
    key=cv2.waitKey(1)
    if key == ord('q') or key==27:
        break  

    if time.time() - start_time > 10:
        print("Se termino el tiempo")
        break


cap.release()
cv2.destroyAllWindows()
sys.exit(0)