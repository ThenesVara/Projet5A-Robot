# Projet5A-Robot

## Lidar
rplidar_a2 : package lidar ROS publisher / subscriber

## Camera
- Générer matrices caméra et distorsion :
camera/camera_calibration_chessboard : Générer des images avec une planche d'échec pour obtenir la matrice de la caméra et les coefficients de distorsion

- Avec les matrices de distorsion et de caméra - Détection aruco et position
camera/camera_test : Détection aruco, position aruco (à implémenter sur la raspberry)
<img src="https://user-images.githubusercontent.com/114569016/212485266-aa58898c-cd93-4f3b-9fb1-195be8e372a9.jpg" width=50% height=50%>

- Optionnel - ne fonctionne pas toujours - Générer matrices caméra et distorsion :
camera/camera_calibration : Générer des images avec une planche aruco pour obtenir la matrice de la caméra et les coefficients de distorsion (parfois erreur)

## MQTT Camera data
Adresse IP à modifier

- Publisher camera aruco :

mqtt_camera_data/ mqtt_publisher_aruco_id_x_y.py : Traite image, détecte position aruco et envoi ces donnees (id,x,y) en mqtt

- Subscriber position aruco :

mqtt_camera_data/ mqtt_subscriber_camera_aruco_data_matrix.py : Souscrit aux donnees de la camera et récupère ces données (mise à jour toutes les x secondes)

## Interface Graphique
Lib: PyQt5

Permetra de suivre en temps réel les déplacements du robot sur l'écran de celui-ci. 
<img src="https://user-images.githubusercontent.com/114569016/215591124-62d49c13-abcd-4f0a-a9ec-cb02d57a6162.png" width=50% height=50%>

Il permettra aussi d'établir une stratégie et de simuler ses déplacements.

