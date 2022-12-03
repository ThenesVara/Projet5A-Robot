#publier id, x, y de l'aruco

import paho.mqtt.client as paho
import time

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

while timer > 1:
    for i in range(len(id)):
        ret= client1.publish("id", id[i])#publish temperature
        time.sleep(0.05)
        ret2= client2.publish("x", 28.1+i)#publish temperature
        time.sleep(0.05)
        ret3= client3.publish("y", 12.1+i)#publish temperature
        time.sleep(0.05)
        
    print("Aruco publie tous les arucos","id, x, y")
    print('timer:',timer)
        
    time.sleep(2) #attend x secs avant de republier
    timer -=2
    
