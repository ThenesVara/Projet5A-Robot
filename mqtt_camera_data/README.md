# Projet5A-Robot

Raspberry Pi (avec caméra) : publisher

Raspi (ou jetson) du robot : subscriber

*mqtt_publisher_aruco_id_x_y.py* : publie aux ids et position x,y à l'adresse IP (choisie) par wifi

*mqtt_subscriber_camera_aruco_data_matrix.py* : souscrit aux ids et position x,y à l'adresse IP (choisie) par wifi sous forme de matrice (qui se met à jour lors d'un changement de position)
                                              [[id1, x1,y1],[id2, x2, y2],...]


## tests
*mqtt_publisher_aruco_id_x_y.py* : envoi les ids et position x,y à l'adresse IP (choisie) par wifi (mqtt)
*mqtt_subscriber_camera_aruco_data_list.py* : souscrit aux ids et position x,y à l'adresse IP (choisie) par wifi (mqtt) sous forme de liste (qui grandit)


*mqtt_publisher_test_aruco_id_x_y.py* : publie aux ids fixe et position fixe x,y à l'adresse IP (choisie) par wifi
*detection_calibration_aruco_position.py* : lance la caméra, détecte les aruco -> 1 aruco de référence, position des autres par rapport à celui là 


## Raspberry Pi

### Librairies

- Mosquitto :

```
sudo apt install -y mosquitto
sudo apt install -y mosquitto-clients
```

- Paho-mqtt :

```
sudo pip3 install paho-mqtt
```

- pip (if needed):

```
sudo apt install python3-pip
```


### Start / stop mosquitto broker

```
sudo systemctl start mosquitto
sudo systemctl start mosquitto.service
sudo systemctl stop mosquitto.service
sudo systemctl restart mosquitto.service
```

Verifier l'etat du broker mqtt :

```
sudo systemctl status mosquitto
```

### Activer tous les clients

```
cd /etc/mosquitto/
```

Modifier le fichier :

```
sudo nano moquitto.conf
```

Ajouter les lignes suivantes sur le fichier :

```
allow_anonymous true
listener 1883 0.0.0.0
```

Erreur rencontrée : https://stackoverflow.com/questions/24556160/mosquitto-client-obtain-refused-connection?fbclid=IwAR0WUCksy6o98-WXznslFZKJHkOA5ck3pmP6M_8lMOtzQn6aqq0ffJl-Jwc

