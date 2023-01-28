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
timer = 20

'''PARAMETRES MQTT'''
#adresse ip de où on envoi les donnees
broker="192.168.200.180"
port=1883

#create client object : topic name
client= paho.Client("nombrearuco")
client1= paho.Client("id")
client2= paho.Client("x")
client3= paho.Client("y")

#establish connection
client.connect(broker,port)
client1.connect(broker,port)
client2.connect(broker,port)
client3.connect(broker,port)




'''PARAMETRES CAMERA / ARUCO'''

#Aruco de réfernce en position 0,0
Aruco_origine = 20

precision = 0.001

compteur = 0

#dimensions image : (longueur, hauteur) = (480, 270) ou (640,480) ou (1920, 1080)
longueur = 1920
hauteur = 1080

cap = cv2.VideoCapture(0)
cap.set(3, longueur)
cap.set(4, hauteur)
cap.set(10, 10) # 10 brightness

#modifier les coefficients cameraMatrix et distcoeff selon les valeurs obtenues après calibration (dans camera/camera_calibration/calibration.yaml)
cameraMatrix = np.array(([1.265975736898479909e+03, 0.0, 1.230683061301125917e+03], [0.0, 1.269892791977853221e+03, 1.031112129345576932e+03], [0., 0., 1.0]))
cameraMatrix = np.reshape(cameraMatrix, (3, 3))
distcoeff = np.array(([-3.067234366049950700e-01, 9.808044863630002719e-02, 1.396706410153973447e-03, 8.297234589805571039e-04,-1.472641965328781548e-02]))
distcoeff = np.reshape(distcoeff, (1, 5))

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
    erreur = np.array(([-14], [-27], [0], [0])) #erreur si besoin de corriger
    coordscorrige = np.add(coords, erreur) #ajoute coeff coords et erreur
    
    # aruco.drawAxis(img, cameraMatrix, distcoeff, rvecs, tvecs, 0.1) #dessine axes
    if ids != Aruco_origine :
        print('\nNum du tag:', ids, '\nCoordonnées:')
        print("x: ", coordscorrige[0])#np.round(coordscorrige[0],3)
        print("y: ", coordscorrige[1])
    
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
                    b=0.0
                    c=0.0
                    compteur = 1
                    
                else:
                    if ids[i] == Aruco_origine:
                        a,b,c= findArucoMarkers(cropped_image, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i], Mcalibinv, ids[i])
                        b=0.0
                        c=0.0
                    else:
                        a, b, c = findArucoMarkers(cropped_image, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i], Mcalibinv, ids[i])
                    
                #PUBLICATION DATA
                ret= client1.publish("nombrearuco", int(len(ids)))#publish id
                time.sleep(0.3)
                ret1= client1.publish("id", int(a))#publish id
                time.sleep(0.3)
                ret2= client2.publish("x", float(b))#publish x
                time.sleep(0.3)
                ret3= client3.publish("y", float(c))#publish y
                time.sleep(0.3)
                pass

    #cv2.imshow("Image", cropped_image)

    cv2.waitKey(1)
    print("Aruco publie tous les arucos","id, x, y")
    print('timer:',timer)

    time.sleep(0.1) #attend x secs avant de republier
    timer -=1.3
