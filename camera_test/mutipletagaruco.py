import cv2
import cv2.aruco as aruco
import numpy as np
import time

cap = cv2.VideoCapture(0)
# cap.set(3, 1920)
# cap.set(4, 1080)

cameraMatrix = np.array(([1318.37800102873, 0.0, 0], [0.0, 1302.16095922522, 0], [520.419216783656, 244.134144200563, 1.0]))
cameraMatrix = np.reshape(cameraMatrix, (3, 3))
distcoeff = np.array(([-0.277568218167406, -0.0692640631211251, 0.0, 0.0]))
distcoeff = np.reshape(distcoeff, (1, 4))

arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_250)
arucoParam = aruco.DetectorParameters_create()


def calibrationArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs, tvecs):

    rvecsTransform, jacobian = cv2.Rodrigues(rvecs)

    t = tvecs
    r = np.array(rvecsTransform)

    Mcalib = np.array(([[r[0][0], r[0][1], r[0][2], t[0][0]],
                        [r[1][0], r[1][1], r[1][2], t[0][1]],
                        [r[2][0], r[2][1], r[2][2], t[0][2]],
                        [0, 0, 0, 1]]))

    Mcalib = np.reshape(Mcalib, (-1, 4))
    Mcalibinv = np.linalg.inv(Mcalib)

    # aruco.drawAxis(img, cameraMatrix, distcoeff, rvecs, tvecs, 0.1);
    return Mcalibinv


def findArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs, tvecs, Mcalibinv, ids):
    ttag = np.array(([tvecs[0][0]], [tvecs[0][1]], [tvecs[0][2]], [1]))
    coords = Mcalibinv.dot(ttag)
    erreur = np.array(([0], [0], [0], [0]))
    coordscorrige = np.add(coords, erreur)
    # aruco.drawAxis(img, cameraMatrix, distcoeff, rvecs, tvecs, 0.1)
    print('Num du tag:\n', ids, '\nCoordonnées:\n')
    print("x: ", coordscorrige[0])
    print("y: ", coordscorrige[1])
    print("")


while True:
    success, img = cap.read()

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
    aruco.drawDetectedMarkers(img, corners)

    rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, 6, cameraMatrix, distcoeff)

    if ids is not None:
        if len(ids) > 0:
            for i in range(len(ids)):
                Mcalibinv = calibrationArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i])
                if ids[i] == 1:
                    Mcalibinv = calibrationArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i])
                elif (Mcalibinv is not None) and (ids[i] != 1):
                    
                    findArucoMarkers(img, corners, cameraMatrix, distcoeff, rvecs[i], tvecs[i], Mcalibinv, ids[i])
                    pass

    cv2.imshow("Image", img)
    cv2.waitKey(1)
