#publier id, x, y des aruco detectes

import paho.mqtt.client as paho
import time

import cv2
import cv2.aruco as aruco
import numpy as np
import time
import math
import decimal

#temps pendant lequel il envoit les positions
timer = 50

# donnee x et y que l'on envoi
global b, c
b=0
c=0

'''PARAMETRES MQTT'''
#adresse ip de où on envoi les donnees
broker="172.20.10.4"
port=1883

## Publie id, x, y (à raspberry robot)
#create client object : topic name
#client1= paho.Client("id")
client2= paho.Client("x")
client3= paho.Client("y")

#establish connection
#client1.connect(broker,port)
client2.connect(broker,port)
client3.connect(broker,port)



'''
 __________________________
|                          |
|   X(3)            X(2)   |
|                      X(o)|
|   X(4)            X(1)   |
|__________________________| 
'''
#Aruco de réfernce en position 0,0
Aruco_origine = 7 #X(0)

## ARUCO FIXES
Aruco_1 = 22
Aruco_2 = 23
Aruco_3 = 21
Aruco_4 = 20

precision = 0.001

compteur = 0


global target 
target = 0
ARUCO_TARGET = [Aruco_2, Aruco_3, Aruco_4, Aruco_1, Aruco_origine]

#dimensions image : (longueur, hauteur) = (480, 270) ou (640,480) ou (1920, 1080)
longueur = 1920
hauteur = 1080

cap = cv2.VideoCapture(0)
cap.set(3, longueur)
cap.set(4, hauteur)
cap.set(10, 10) # 10 brightness

#modifier les coefficients cameraMatrix et distcoeff selon les valeurs obtenues après calibration
cameraMatrix = np.array(([1.265975736898479909e+03, 0.0, 1.230683061301125917e+03], [0.0, 1.269892791977853221e+03, 1.031112129345576932e+03], [0., 0., 1.0]))
cameraMatrix = np.reshape(cameraMatrix, (3, 3))
distcoeff = np.array(([-3.067234366049950700e-01, 9.808044863630002719e-02, 1.396706410153973447e-03, 8.297234589805571039e-04,-1.472641965328781548e-02]))
distcoeff = np.reshape(distcoeff, (1, 5))

arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_50)
arucoParam = aruco.DetectorParameters_create()


        



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
    
    # aruco.drawAxis(img, cameraMatrix, distcoeff, rvecs, tvecs, 0.1) #dessine axes
    if ids != Aruco_origine and ids !=Aruco_1 and ids != Aruco_2 and ids != Aruco_3 and ids !=Aruco_4:
        print('\nNum du tag:', ids, '\nCoordonnées:')
        print("x: ", coordscorrige[0])
        print("y: ", coordscorrige[1])
        
    if ids == Aruco_origine :
        coordscorrige[0] = 0
        coordscorrige[1] = 0
#         print('ORIGINE')
#         print("x0: ", coordscorrige[0])
#         print("y0: ", coordscorrige[1])
        
    ## ARUCO FIXES 
    if ids == Aruco_1 :
        coordscorrige[0] = -44
        coordscorrige[1] = 30
#         print("x1: ", coordscorrige[0])
#         print("y1: ", coordscorrige[1])
        
    if ids == Aruco_2 :
        coordscorrige[0] = 42
        coordscorrige[1] = 30
#         print("x2: ", coordscorrige[0])
#         print("y2: ", coordscorrige[1])
        
    if ids == Aruco_3 :
        coordscorrige[0] = 42
        coordscorrige[1] = 215
#         print("x3: ", coordscorrige[0])
#         print("y3: ", coordscorrige[1])
        
    if ids == Aruco_4 :
        coordscorrige[0] = -44
        coordscorrige[1] = 215
#         print("x4: ", coordscorrige[0])
#         print("y4: ", coordscorrige[1])
    
    return ids, coordscorrige[0], coordscorrige[1]
    


while timer > 1:
    success, img = cap.read()
    
    #crop image pour limiter la table
    cropped_image = img[35:hauteur-150, 60:longueur-60]
    
    #on transforme l'image en gris pour mieux detecter
    imgGray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(cropped_image, arucoDict, parameters=arucoParam)
    
    #corners = position coins aruco -> [coin rouge, .., .., ..]
    aruco.drawDetectedMarkers(cropped_image, corners)

    #rvec vecteur rotation, tvecs position x,y,z
    rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, 6, cameraMatrix, distcoeff)

    if ids is not None:
        if len(ids) > 0:
            for i in range(len(ids)):
                #Détecte dans la zone crop l'aruco d'origine (0,0)
                if ids[i] == Aruco_origine and compteur == 0:
                    #cropped_image = img[int(hauteur/2)-100:hauteur-170, int(longueur/2)+50:longueur-80]
                    Mcalibinv = calibrationArucoMarkers(cropped_image, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i])
                    a,b,c= findArucoMarkers(cropped_image, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i], Mcalibinv, ids[i])
                    compteur = 1
                    
                else:
                    if ids[i] == Aruco_origine:
                        a, b, c = findArucoMarkers(cropped_image, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i], Mcalibinv, ids[i])

                    else:
                        a, b, c = findArucoMarkers(cropped_image, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i], Mcalibinv, ids[i])
                                 
                    
                #PUBLICATION DATA
                if ids[i]== ARUCO_TARGET[target]:
                    #ret1= client1.publish("id", int(a))#publish id
                    #time.sleep(0.3)
                    ret2= client2.publish("x", float(c))#publish x
                    time.sleep(0.3)
                    ret3= client3.publish("y", float(b))#publish y
                    time.sleep(0.3)
                    pass

    #cv2.imshow("Image", cropped_image)

    cv2.waitKey(1) 
    print("Aruco publie tous les arucos","id, x, y")
    print('timer:',timer)

    time.sleep(0.1) #attend x secs avant de republier
    timer -= 0.7    




