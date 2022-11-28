Code inspiré de : https://github.com/abakisita/camera_calibration

# Générer des images avec la planche Aruco 

1. Imprimer la planche Aruco : aruco.DICT_4X4_50 

![aruco_marker_board_4x4](https://user-images.githubusercontent.com/114569016/204263849-82a971af-ae55-43cb-b95a-8db3d110595d.png)


2. Data_generation.py : 
- Modifier le chemin où les images sont enregistrées
- Prendre environ 50 images de la planche Aruco imprimée sous différents angles, distance.

![8](https://user-images.githubusercontent.com/114569016/204263889-36132254-4a5c-4d54-bccf-4d0d237ca09f.jpg)


## Calibrating camera
1. Sur la planche Aruco imprimée : Mesurer la taille d'un tag Aruco et la distance entre 2 Aruco

2. camera_calibration.py : 
- Modifier markerLength et markerSeparation (par rapport aux valeurs mesurés)
- Modifier la bibliothèque aruco utilisée (selon la planche utilisée) : aruco_dict = ... DICT_4X4_50 (ou autre)

3. Lancer le code camera_calibration.py

4. Ce code va générer des matrices dans calibration.yaml avec les coefficients de matrice de la caméra et les coefficients de distorsion


