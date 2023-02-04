''' S'abonne en mqtt aux topics id,x,y (aruco), recupere donnees sous forme de matice'''

import paho.mqtt.client as mqtt
import numpy 


broker_address = "172.20.10.4"  # Broker address
port = 1883  # Broker port


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([("x", 1), ("y", 1)])

    
#coordonees enregistrees dans list
global list
list = numpy.array([0.,0.,0.])
list_temporaire = []
i=0

def on_message(client, userdata, message):
    #liste_temporaire enregistre id et position x,y associé (si pas de list_temporaire,)
    #lorsque on obtient toutes les valeurs -> ajoute dans list les valeurs id,x,y de list_temporaire
    #list_temporaire est remis à 0 ensuite

    global list_temporaire, i

    taille_message = len(str(message.payload))
    msg = str(message.payload)[2:taille_message-1]
    print("Message received: " + message.topic + " : " + msg)


    if message.topic == 'x':
        list_temporaire = numpy.append(list_temporaire,[float(msg)])
        i+=1


    if message.topic == 'y':
        list_temporaire = numpy.append(list_temporaire,[float(msg)])
        i+=1

        
    if i >=2 :
        for i in range(0,2):
            list[i] = list_temporaire[i]
        i=0
        list_temporaire = []




#protocole TLS : securisé ----------- > https://www.frugalprototype.com/mqtt-tls/
#user = "rir"      #Connection username
#password = "rir"  #Connection password

client = mqtt.Client()  # create new instance
client.on_connect = on_connect  # attach function to callback
client.on_message = on_message  # attach function to callback
#client.username_pw_set(username = user, password = password)    #set username and password

client.connect(broker_address, port=port)  # connect to broker

client.loop_forever()
