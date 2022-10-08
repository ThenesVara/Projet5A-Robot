BIBLIOTHEQUE RPLIDAR:
- baudrate = 115200 #rplidarA2M8
- max_buf_meas = 5000 -> modifiable


Dans : test_lidar_angle.py, test_lidar.py, subscriber_lidar_distance.py 
MODIFIER : password  ----> subprocess.Popen(“echo password | sudo -S chmod 666 /dev/ttyUSB0”, stdout=subprocess.PIPE,shell=True) 





TESTS :
test_lidar_angle.py     : lance le lidar et détecte points sur un certain angle et inférieur à une distance
test_lidar.py           : lance le lidar et détecte points inférieur à une distance 

SCRIPTS :
publisher_lidar_distance.py : publie la distance entre l’obstacle et le lidar en continu (avec seuil minimum et un angle défini)
subscriber_lidar_distance.py : souscrit à publisher_lidar_distance.py

LAUNCH :
ros_pub_subs_lidar.launch : lance node publisher et subcriber du lidar distance



Terminal :
$ source /lidar_ws/devel/setup.bash 
$ roslaunch rplidar_a2 ros_pub_subs_lidar.launch  