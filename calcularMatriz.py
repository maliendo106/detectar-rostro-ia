from flask import Flask, request, json, jsonify
import cv2
import face_recognition
import numpy as np
import base64
import json
from flask_cors import CORS
import re
import time
import subprocess

app = Flask(__name__)
CORS(app, methods=['GET', 'POST', 'PUT', 'DELETE'], allow_headers=['Content-Type', 'Authorization'])
start_time = None

@app.post('/calcular-matriz')
def calcular():

    try:
        data = request.json
        image = data["imagen64"]
        image = str(image).replace(" ", "")
        # print(f"imagenbase64: {image}")
        image = base64.b64decode(image)
        # print(f"imagendata: {image}")
        
        image = np.frombuffer(image, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
        faces_loc=face_recognition.face_locations(image)

        faces = []
        for fl in faces_loc:
            model=face_recognition.face_encodings(image, known_face_locations=[fl])
            face_array = np.array(model)
            flattened_array = face_array.flatten().tolist()
            hola = str(flattened_array).replace("'", "").replace("[", "").replace("]", "").replace(",", "")
            faces.append(hola)
              
        response = jsonify(matriz=faces)
        response.status_code = 200
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response

    except Exception as e:
        print(e)
        response = jsonify(error=e)
        response.status_code = 500
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        return response
    
@app.post('/detectar-rostro')
def detectar():
    
    try:
        data = request.json
        matriz = data["matriz"]
        with open("perfil.txt", "w") as file:
            file.write(matriz)
        output = subprocess.check_output(["python", "IdentificaRostro.py"])
        output = output.decode("utf-8")
        print("AAAAAAAAAAAA: ",output)
        response = jsonify(msg=output)
        response.headers["Content-Type"] = "application/json; charset=utf-8"
        if(output[0] == "1"):
            response.status_code = 200
        else:
            response.status_code = 403
        return response
        
    except Exception as e:
        print(e)
        
    
    return "a"
    # try:
        
    #     data = request.json
    #     matriz = data["matriz"]
    #     with open("perfil.txt", "w") as file:
    #         file.write(matriz)
    #     matriz = np.loadtxt("./perfil.txt")

    #     cap=cv2.VideoCapture(0)
    #     global start_time
    #     start_time = time.time()

    #     while True:
    #         ret, frame=cap.read()
    #         if ret == False:
    #             break

    #         frame=cv2.flip(frame,1)
    #         faces_loc=face_recognition.face_locations(frame)
    #         for fl in faces_loc:
    #             model=face_recognition.face_encodings(frame, known_face_locations=[fl])
    #             result=False
    #             for f in model:
    #                 result = result or True in face_recognition.compare_faces([matriz],f)
    #             quien="Desconocid@"
    #             if result:
    #                 cap.release()
    #                 cv2.destroyAllWindows()
    #                 start_time = time.time()
    #                 quien=""
    #                 response = jsonify(data="hola")
    #                 response.status_code = 200
    #                 response.headers["Content-Type"] = "application/json; charset=utf-8"
    #                 return response
  
    #             cv2.rectangle(frame, (fl[3], fl[2]), (fl[1], fl[2]+30), (50,50,255), -1 )
    #             cv2.rectangle(frame, (fl[3], fl[0]), (fl[1], fl[2]), (50,50,255), 2 )
    #             cv2.putText(frame, quien , (fl[3], fl[2]+20),2,0.7,(255,255,255), 1)

    #         cv2.imshow('video', frame)
    #         key=cv2.waitKey(1)
    #         if key == ord('q') or key==27:
    #             break  

    #         if time.time() - start_time > 10:
    #             print("Se termino el tiempo")
    #             break

        
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     response = jsonify(data="hola")
    #     response.status_code = 400
    #     response.headers["Content-Type"] = "application/json; charset=utf-8"
    #     return response
        
    # except Exception as e:
    #     cap.release()
    #     cv2.destroyAllWindows()
    #     response = jsonify(data=e)
    #     response.status_code = 500
    #     response.headers["Content-Type"] = "application/json; charset=utf-8"
    #     return response
        

if __name__ == '__main__':
    app.run(debug=True, host='192.168.192.6', port=8100)