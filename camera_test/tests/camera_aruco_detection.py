'''open camera and detect aruco
   return numero aruco 
'''

'''https://www.youtube.com/watch?v=AQXLC2Btag4'''

import cv2
import cv2.aruco as aruco


VideoCap=True
cap=cv2.VideoCapture(0)


# marker_size=4 
def findAruco(img, marker_size=4, total_markers=50, draw=True):
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	key=getattr(aruco, f'DICT_{marker_size}X{marker_size}_{total_markers}')
	arucoDict = aruco.Dictionary_get(key)
	arucoParam = aruco.DetectorParameters_create()
	bbox, ids,_=aruco.detectMarkers(gray,arucoDict,parameters=arucoParam)
	print(ids)
	if draw:
		aruco.drawDetectedMarkers(img,bbox)
	
	return bbox, ids

while True:
	VideoCap, img=cap.read()
	bbox,ids=findAruco(img)
	if cv2.waitKey(1)==110:
		break
	cv2.imshow("img",img)