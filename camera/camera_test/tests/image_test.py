'''open image'''

from PIL import Image

#Image aruco
path = '/home/rir/Desktop/camera_test/Aruco/Aruco_jaune.png' 

im = Image.open(path) 
im.show() 