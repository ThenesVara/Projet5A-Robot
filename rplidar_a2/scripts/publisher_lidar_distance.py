#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from rplidar import RPLidar
import subprocess
from rplidar_a2.msg import Distance


subprocess.Popen("echo 'password' | sudo -S  chmod 666 /dev/ttyUSB0", stdout=subprocess.PIPE, shell=True)
lidar = RPLidar('/dev/ttyUSB0') #vérifier COM : gestionnaires des périphériques -> Ports (COM et LPT) (enlever et remettre le lidar pour etre sûr du COM)


seuil = 300 #millimiters


def scan():
    pub = rospy.Publisher('lidar_topic',Distance, queue_size=10) #Publisher('topic_name', topic type, queue_size)
    rospy.init_node('publish_lidar_node', anonymous=True)#initialise node : ('node_name', anonymous -> si 2 fois le meme node pourra distinguer node-1 et node-2)
    rate = rospy.Rate(40) #frequence de publication -> f=1/t donc attend t=1/f secondes avant de republier 
    rospy.loginfo("Publisher Node Started")
    
    distance = 400

    while not rospy.is_shutdown():
        msg=Distance()
        #msg.message = "Distance to obstacle:"
        '''msg.obstacle_distance = distance
        pub.publish(msg) #msg qu'il publie
        rate.sleep()'''

        distance = 400
        
        #iter_scan -> [quality,angle,distance]
        for i, scan in enumerate(lidar.iter_scans()):
            #print('%d: Got %d measurments' % (i, len(scan))) #nombre de points
            msg.obstacle_distance = distance
            pub.publish(msg) #msg qu'il publie
            rate.sleep()
            distance = 400

            for j in range (len(scan)):
                #récupere toutes les informations de distances
                '''iter_scan : [scan[j][0]=quality, scan[j][1]= angle, scan[j][2]=distance] '''

                if (scan[j][1]>0 and scan[j][1]<90 and scan[j][2] < seuil):
                    distance = scan[j][2]
                     
  
            if i > 1000:
                break
        
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

'''
def stoplidar():
    #stop lidar
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
'''    



if __name__ == '__main__':
    try:
        scan()
    except rospy.ROSInterruptException:
        pass    