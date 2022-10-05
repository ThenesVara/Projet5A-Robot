#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from rplidar import RPLidar
from rplidar_a2.msg import Distance

def callback(data):
    #rospy.loginfo("Received Data: %s", data.data) #data.data
    rospy.loginfo("%f", data.obstacle_distance)

def listener():
    rospy.init_node("subscriber_lidar_node", anonymous = True)
    rospy.Subscriber('lidar_topic', Distance, callback) #rospy.Subscriber(topic_to_subscribe, type_msg_to_receive, callback) -> callback is the function which get data
    rospy.spin()# spin => let run node continuously until we stop node


if __name__ == '__main__':
    try: 
        listener()
    except rospy.ROSInterruptException:
        pass