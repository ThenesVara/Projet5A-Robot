'''This script is for generating data
1. Provide desired path to store images.
2. Press 'c' to capture image and display it.
3. Press any button to continue.
4. Press 'q' to quit.
'''

import cv2
import time

camera = cv2.VideoCapture(0)
camera.set(3, 480)
camera.set(4, 270)
ret, img = camera.read()


path = "/home/rir/Desktop/camera_calibration/aruco_data/"
count = 0
nombreimages = 45

while count < nombreimages:
    name = path + str(count)+".jpg"
    ret, img = camera.read()

    time.sleep(1)
    cv2.imwrite(name, img)
    cv2.imshow("img", img)
    count += 1
        
