'''open image'''

from PIL import Image

#Image aruco
path = 'Aruco/Aruco_jaune.png' 

im = Image.open(path) 
im.show() 