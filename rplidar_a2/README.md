# RPLIDAR A2M8
![rplidar_A2](https://user-images.githubusercontent.com/114569016/194724487-ec93e4c6-d517-4d5d-92f5-d973ee842cca.png)

# Bibliothèque RPLIDAR:
1- Install rplidar library
```
pip install rplidar
```
Or for Python3
```
pip install rplidar
```

2- Configuration

For rplidarA2M8, rplidarA2M6 :
- baudrate = 115200 
- max_buf_meas = 5000 -> modifiable

![image](https://user-images.githubusercontent.com/114569016/194724324-31ccc1e7-85a5-4b88-bf4d-4317c9abfb5c.png)
![image](https://user-images.githubusercontent.com/114569016/194724335-c05c54ad-36ab-4095-be41-50d9d5f87fb4.png)
![image](https://user-images.githubusercontent.com/114569016/194724336-92a232e6-9f78-4750-883d-249607f048d7.png)

For rplidarA2M7, rplidarA3 :
- baudrate = 256000 
- max_buf_meas = 5000 -> modifiable

# Fichiers
## Tests :
*test_lidar_angle.py*     : lance le lidar et détecte points sur un certain angle et inférieur à une distance

*test_lidar.py*           : lance le lidar et détecte points inférieur à une distance 

**MODIFIER dans le code** : subprocess.Popen(“echo **password** | sudo -S chmod 666 /dev/ttyUSB0”, stdout=subprocess.PIPE,shell=True) 

## Scripts :
*subscriber_lidar_distance.py* : souscrit à publisher_lidar_distance.py

*publisher_lidar_distance.py* : publie la distance entre l’obstacle et le lidar en continu (avec seuil minimum et un angle défini)

**MODIFIER dans le code** : subprocess.Popen(“echo **password** | sudo -S chmod 666 /dev/ttyUSB0”, stdout=subprocess.PIPE,shell=True) 

## Launch :
*ros_pub_subs_lidar.launch* : lance node publisher et subcriber du lidar distance

```
source /lidar_ws/devel/setup.bash 
roslaunch rplidar_a2 ros_pub_subs_lidar.launch  
```




