''' S'abonne en mqtt aux topics id,x,y (aruco), recupere donnees sous forme de liste'''

import paho.mqtt.client as mqtt
import numpy as np


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("id", 1), ("x", 1), ("y", 1)])

list = np.array([])
list_temporaire = []
i=0

def on_message(client, userdata, message):
    #liste_temporaire enregistre id et position x,y associé (si pas de list_temporaire,)
    #lorsque on obtient toutes les valeurs -> ajoute dans list les valeurs id,x,y de list_temporaire
    #list_temporaire est remis à 0 ensuite

    global list, list_temporaire, i

    taille_message = len(str(message.payload))
    msg = str(message.payload)[2:taille_message-1]
    print("Message received: " + message.topic + " : " + msg)

    
    #id est un entier et x,y des nombres decimaux
    if message.topic == 'id':
        list_temporaire = np.append(list_temporaire,[int(msg)])
        i+=1


    if message.topic == 'x':
        list_temporaire = np.append(list_temporaire,[float(msg)])
        i+=1


    if message.topic == 'y':
        list_temporaire = np.append(list_temporaire,[float(msg)])
        i+=1

        
    if i >=3 :
        list = np.append(list, list_temporaire)
        i=0
        list_temporaire = []

    print('list',list)
    #print(np.size(list))




broker_address = "localhost"  # Broker address
port = 1883  # Broker port

#protocole TLS : securisé ----------- > https://www.frugalprototype.com/mqtt-tls/

# user = "yourUser"                    #Connection username
# password = "yourPassword"            #Connection password

client = mqtt.Client()  # create new instance
# client.username_pw_set(user, password=password)    #set username and password
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback

client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()