Code de : https://github.com/tizianofiorenzani/how_do_drones_work/tree/master/opencv

# Générer des images avec la planche Aruco 

1. Imprimer la planche Aruco : ChessBoard_9x6 

2. dataset/generate_dataset.py : 
- Prendre environ 50 images de la planche Aruco imprimée sous différents angles, distance.


## Calibrating camera
1. Sur la planche Aruco imprimée : Mesurer la taille d'un tag Aruco et la distance entre 2 Aruco

2. camera_calibration.py : 
- Modifier dimension 
- Modifier path : workingForlder

3. Lancer le code camera_calib.py

4. Ce code va générer des matrices de camera et Distorsion dans : cameraMatrix.txt et cameraDistorsion.txt

