# Fichiers

## Tests :
Utilisation de la librairie : aruco.DICT_4X4_50 

*camera_aruco_detection.py*  : lance la caméra et détecte les aruco, numero aruco (id)

- Utile pour savoir l'id de votre aruco de référence

*camera_test.py*             : lance la caméra

*crop_camera_test.py*        : lance la caméra avec une image recadré

*image_aruco_test.py*        : ouvre une image aruco et détecte 

*image_test.py*              : ouvre une image

## Code :
*detection_calibration_aruco_position* : lance la caméra, détecte les aruco -> 1 aruco de référence, position des autres par rapport à celui là 

![1](https://user-images.githubusercontent.com/114569016/212485266-aa58898c-cd93-4f3b-9fb1-195be8e372a9.jpg)


## Raspberry Pi
- Activer camera : 
```
sudo raspi-config
```
Aller dans Interface Option - Legacy Camera. Ensuite : enable camera

- Activer d'autres options : Aller dans configuration du Raspberry Pi, dans l'onglet Interfaces et activer les options utiles comme SSH.

- Redémarrer la raspberry : 
```
reboot
```

- Installer la librairie OpenCV : 

```
sudo apt install python3-opencv
```

## Aruco
Images aruco utilisés

id :

jaune = 13

marron = 36

rose = 47

bleu1 = 2 

bleu2 = 1

vert1 = 7

vert2 = 6

table1 = 20

table2 = 21

table3 = 22

table4 = 23

