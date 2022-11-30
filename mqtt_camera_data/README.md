# Projet5A-Robot

## Raspberry Pi (avec caméra)

mqtt_publisher_aruco_id_x_y.py : envoi les ids et position x,y à l'adresse IP (choisie) par wifi (mqtt)

## Rasp / Jetson

mqtt_subscriber_camera_aruco_data_list.py : récupère les ids et position x,y (envoyé par la raspberry avec la caméra) -> sous forme de liste

mqtt_subscriber_camera_aruco_data_matrix.py : récupere les ids et position x,y (envoyé par la raspberry avec la caméra) sous forme de matrice et met à jour la matrice 
[[id1, x1,y1],
 [id2, x2, y2],...]


