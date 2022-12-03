#publier id, x, y des aruco detectes

import paho.mqtt.client as paho
import time

import cv2
import cv2.aruco as aruco
import numpy as np
import math
import decimal



'''PARAMETRES MQTT'''
#temps pendant lequel il envoit les positions
timer = 20

#adresse ip de où on envoi les donnees
broker="192.168.200.180"
port=1883

#create client object : topic name
client1= paho.Client("id")
client2= paho.Client("x")
client3= paho.Client("y")

#establish connection
client1.connect(broker,port)
client2.connect(broker,port)
client3.connect(broker,port)


'''PARAMETRES CAMERA / ARUCO'''
cap = cv2.VideoCapture(0)
cap.set(3, 480) #cap.set(3, 1920)
cap.set(4, 270) #cap.set(4, 1080)

#modifier les coefficients cameraMatrix et distcoeff selon les valeurs obtenues après calibration (dans camera/camera_calibration/calibration.yaml)
cameraMatrix = np.array(([1318.37800102873, 0.0, 0], [0.0, 1302.16095922522, 0], [520.419216783656, 244.134144200563, 1.0]))
cameraMatrix = np.reshape(cameraMatrix, (3, 3))
distcoeff = np.array(([-0.277568218167406, -0.0692640631211251, 0.0, 0.0]))
distcoeff = np.reshape(distcoeff, (1, 4))

arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
arucoParam = aruco.DetectorParameters_create()

'''FONCTIONS CAMERA'''
def calculateDistance(x1,y1,x2,y2):
    dist=math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return dist

def calibrationArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs, tvecs):
    rvecsTransform, jacobian = cv2.Rodrigues(rvecs)
    t = tvecs
    r = np.array(rvecsTransform)
    Mcalib = np.array(([[r[0][0], r[0][1], r[0][2], t[0][0]],
                        [r[1][0], r[1][1], r[1][2], t[0][1]],
                        [r[2][0], r[2][1], r[2][2], t[0][2]],
                        [0, 0, 0, 1]]))

    Mcalib = np.reshape(Mcalib, (-1, 4))
    Mcalibinv = np.linalg.inv(Mcalib)
    # aruco.drawAxis(img, cameraMatrix, distcoeff, rvecs, tvecs, 0.1);
    return Mcalibinv

def findArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs, tvecs, Mcalibinv, ids):
    ttag = np.array(([tvecs[0][0]], [tvecs[0][1]], [tvecs[0][2]], [1]))#position : longueur, largeur, profondeur, 1
    coords = Mcalibinv.dot(ttag) #recalibre pour mettre à 0
    erreur = np.array(([0], [0], [0], [0])) #erreur si besoin de corriger
    coordscorrige = np.add(coords, erreur) #ajoute coeff coords et erreur  
    #aruco.drawAxis(img, cameraMatrix, distcoeff, rvecs, tvecs, 0.1) #dessine axes
    
    #arrondi les valeurs envoyés
    print('\nNum du tag:', ids, '\nCoordonnées:')
    print("x: ", round(coordscorrige[0][0],3))
    print("y: ", round(coordscorrige[1][0],3))    
    return ids, round(coordscorrige[0][0],3), round(coordscorrige[1][0],3)




while timer > 1:
    
    success, img = cap.read()
    
    #on transforme l'image en gris pour mieux detecter
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    
    #corners = position coins aruco -> [coin rouge, .., .., ..]
    aruco.drawDetectedMarkers(img, corners)

    #rvec vecteur rotation, tvecs position x,y,z
    rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, 6, cameraMatrix, distcoeff)

    if ids is not None:
        if len(ids) > 0:
            for i in range(len(ids)):            
                #Aruco initial -> reference (0,0) par rapport aux autres
                if ids[i] == 1:
                    Mcalibinv = calibrationArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i])
                    a,b,c = findArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i], Mcalibinv, ids[i])
                    
                else:
                #elif (Mcalibinv is not None) and (ids[i] != 1):  
                    a,b,c = findArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i], Mcalibinv, ids[i])
                    pass
                
                ret= client1.publish("id", int(a))#publish temperature
                time.sleep(0.3)
                ret2= client2.publish("x", float(b))#publish temperature
                time.sleep(0.3)
                ret3= client3.publish("y", float(c))#publish temperature
                time.sleep(0.3)
                
 
    #cv2.imshow("Image", img)
    cv2.waitKey(1)
      
    print("Aruco publie tous les arucos","id, x, y")
    print('timer:',timer)
        
    time.sleep(2) #attend x secs avant de republier
    timer -=2