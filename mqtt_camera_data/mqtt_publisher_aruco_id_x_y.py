#publier id, x, y de l'aruco

import paho.mqtt.client as paho
import time
from datetime import datetime

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

id = [1, 5, 7, 8, 27]
nbre_id = len(id)

while timer > 1:
    for i in range(nbre_id):
        ret= client1.publish("id", i)#publish temperature
        ret2= client2.publish("x", 28.2+i)#publish temperature
        ret3= client2.publish("y", 12.1+i*3)#publish temperature
        
    print("Aruco publie tous les aruco","id","x","y")
        
    time.sleep(2) #attend x sec
    timer -=2
