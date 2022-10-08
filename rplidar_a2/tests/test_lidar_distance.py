from rplidar import RPLidar
import time
import subprocess

# Le lidar détecte les points sur une distance seuil défini

PORT_NAME = '/dev/ttyUSB0'

#Autorisation usb lidar
subprocess.Popen("echo 'password' | sudo -S  chmod 666 /dev/ttyUSB0", stdout=subprocess.PIPE, shell=True) #modifier password

lidar = RPLidar(PORT_NAME)  #vérifier COM : gestionnaires des périphériques -> Ports (COM et LPT) (enlever et remettre le lidar pour etre sûr du COM)


seuil = 300 #distance critique (trop proche) en mm
time.sleep(2) #pour eviter erreur : Wrong Body size -> laisser le temps au lidar de se lancer

for i, scan in enumerate(lidar.iter_scans()):
    #print('%d: Got %d measurments' % (i, len(scan))) #nombre de points
    for j in range (len(scan)):
        #récupere toutes les informations de distances
        #print('distance', scan[j][2] ) #iter_scan -> [quality,angle,distance]
        if scan[j][2] < seuil:
            print("TROP PROCHE")
            print('distance', scan[j][2] )
    
    if i > 100:
        break


lidar.stop()
lidar.stop_motor()
lidar.disconnect()








'''
#information about lidar (model, serialnumber...)
info = lidar.get_info()
print(info)

#information about health of lidar 
health = lidar.get_health()
print(health)'''
