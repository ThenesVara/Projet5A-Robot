#-------------------------------------------------------------------------------
# Name:        Serial_comm
# Purpose:     Communication entre la carte interface graphique et la carte de trajectoire à travers une liaison série. 
#
# Author:      aymeric
#
# Created:     12/07/2021
# Copyright:   (c) aymeric 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import serial
#cette fonction permet de récupérer les infos de la carte qui gére les trajectoires et de les envoyer à la carte qui gère l'interface graphique 
def serial_comm():
    x=""
    X=""        
    ser=serial.Serial('com22',115200)
    while True:
        ser.write(1)
        x=ser.read(4)
        ser.write(0)
        if x[1]!=0:
            print(1)
            for i in range(len(x)):
                X+=chr(x[i])
            ser.close()
            print(X)
            return X
#serial_comm()