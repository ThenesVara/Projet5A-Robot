# Fichiers
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

## Tests :
Utilisation de la librairie : aruco.DICT_4X4_50 

*camera_aruco_detection.py*  : lance la caméra et détecte les aruco, numero aruco (id)
*camera_test.py*             : lance la caméra
*image_aruco_test.py*        : ouvre une image aruco et détecte 
*image_test.py*              : ouvre une image

*tag_aruco.py*               : 

## Code :
*detection_calibration_aruco_position* : lance la caméra, détecte les aruco -> 1 aruco de référence, position des autres par rapport à celui là 

## Raspberry Pi
- Activer camera : sudo raspi-config

Aller dans Interface Option - Legacy Camera. Ensuite : enable camera

- Activer d'autres options : Aller dans configuration du Raspberry Pi, dans l'onglet Interfaces et activer les options utiles comme SSH.

- Installer la librairie OpenCV : sudo apt install python3-opencv
