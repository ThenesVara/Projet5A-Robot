#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from rplidar import RPLidar
import subprocess
from rplidar_a2.msg import Distance

# Le lidar publie infos quand inférieur au seuil et dans l'angle défini

PORT_NAME = '/dev/ttyUSB0'

subprocess.Popen("echo 'password' | sudo -S  chmod 666 /dev/ttyUSB0", stdout=subprocess.PIPE, shell=True)
lidar = RPLidar(PORT_NAME) #vérifier COM : gestionnaires des périphériques -> Ports (COM et LPT) (enlever et remettre le lidar pour etre sûr du COM)


seuil = 300 #millimiters

def stoplidar():
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()


def scan():
    pub = rospy.Publisher('lidar_topic',Distance, queue_size=10) #Publisher('topic_name', topic type, queue_size)
    rospy.init_node('publish_lidar_node', anonymous=True) #initialise node : ('node_name', anonymous -> si 2 fois le meme node pourra distinguer node1 et node2)
    rate = rospy.Rate(40) #frequence de publication -> f=1/t donc attend t=1/f secondes avant de republier 
    rospy.loginfo("Publisher Node Started")
    
    distance = seuil+100

    while not rospy.is_shutdown():
        msg=Distance()
        distance = seuil+100
        
        #iter_scan -> [quality,angle,distance]
        for i, scan in enumerate(lidar.iter_scans()):
            
            if distance < seuil :
                #publie msg si obstacle < seuil
                msg.obstacle_distance = distance
                pub.publish(msg) 
                rate.sleep()

            distance = seuil+100 #reinitialise distance 

            for j in range (len(scan)):
                '''iter_scan : [scan[j][0]=quality, scan[j][1]= angle, scan[j][2]=distance] '''

                #teste si 90>angle>0 et distance<seuil => 1 info distance par tour pour éviter trop infos
                if (scan[j][1]>0 and scan[j][1]<90 and scan[j][2] < seuil):
                    distance = scan[j][2] 
                     
            
            if i > 1000:
                break
        
    #arrete le lidar à la fin
    stoplidar()





if __name__ == '__main__':
    try:
        scan()
    except rospy.ROSInterruptException:
        pass    