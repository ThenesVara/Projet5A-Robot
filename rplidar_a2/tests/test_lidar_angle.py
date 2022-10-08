from rplidar import RPLidar
import time
import subprocess

# Le lidar détecte les points sur une distance seuil défini et dans une range (angle) bien définie

'''
VOIR IMAGE

                sens du lidar

                angle : 0 deg

                    ^      
                    |
  280 deg <-------lidar-------- > 90 degres
                    |
                    v
                angle : 180 deg   
           
                    ||  
                    ||
                    ||     

'''
PORT_NAME = '/dev/ttyUSB0'

#Autorisation usb lidar automatiquement (2eme essai et suivant fonctionnent)
subprocess.Popen("echo 'password' | sudo -S  chmod 666 /dev/ttyUSB0", stdout=subprocess.PIPE, shell=True) #modifier password


lidar = RPLidar(PORT_NAME)  #vérifier COM : gestionnaires des périphériques -> Ports (COM et LPT) (enlever et remettre le lidar pour etre sûr du COM)


seuil = 300 #distance critique (trop proche) en mm

time.sleep(2) #pour eviter erreur : Wrong Body size -> laisser le temps au lidar de se lancer




for i, scan in enumerate(lidar.iter_scans()):
    #print('%d: Got %d measurments' % (i, len(scan))) #nombre de points
    for j in range (len(scan)):
        #récupere toutes les informations de distances
        #print('distance', scan[j][2] ) #iter_scan -> [quality,angle,distance]

        ''' SEUIL_ANGLE2 > ANGLE > SEUIL_ANGLE1'''
        if (scan[j][1]>0 and scan[j][1]<90):
            #print("Angle actuel: %s ", scan[j][1])

            ''' DISTANCE < SEUIL'''
            if scan[j][2] < seuil:
                print("Angle", scan[j][1]) 
                print("TROP PROCHE")
                print('distance', scan[j][2] )
    
    if i > 100:
        break


lidar.stop()
lidar.stop_motor()
lidar.disconnect()
