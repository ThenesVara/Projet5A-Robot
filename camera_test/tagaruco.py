import cv2
import cv2.aruco as aruco
import numpy as np
import time

cameraMatrix = np.array(([1318.37800102873, 0.0, 0], [0.0, 1302.16095922522, 0], [520.419216783656, 244.134144200563, 1.0]))
cameraMatrix = np.reshape(cameraMatrix, (3, 3))
distcoeff = np.array(([-0.277568218167406, -0.0692640631211251, 0.0, 0.0]))
distcoeff = np.reshape(distcoeff, (1, 4))

calibration = False
Mcalib = np.array((4, 4))

def calibrationArucoMarkers(img, draw=True, position=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_100)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)

    if draw:
        aruco.drawDetectedMarkers(img, corners)

    if ids is not None:
        for marker in ids:
            if position and ids[0] == 1:
                rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, 6, cameraMatrix, distcoeff)
                if rvecs is not None:
                    rvecsTransform, jacobian = cv2.Rodrigues(rvecs)

                    t = tvecs
                    r = np.array(rvecsTransform)

                    Mcalib = np.array(([[r[0][0], r[0][1], r[0][2], t[0][0][0]],
                                        [r[1][0], r[1][1], r[1][2], t[0][0][1]],
                                        [r[2][0], r[2][1], r[2][2], t[0][0][2]],
                                        [0, 0, 0, 1]]))

                    Mcalib = np.reshape(Mcalib, (-1, 4))
                    Mcalibinv = np.linalg.inv(Mcalib)
                    # print(Mcalib)
                    # print("")
                    # print(Mcalibinv)
                    # print("--fin--")
                    return Mcalibinv


def findArucoMarkers(img, Mcalibinv, draw=True, position=True):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = aruco.Dictionary_get(aruco.DICT_4X4_100)
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)

    if draw:
        aruco.drawDetectedMarkers(img, corners)

    if ids is not None:
        for marker in ids:
            if position and ids[0] != 1:
                rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, 0.06, cameraMatrix, distcoeff)
                if tvecs is not None:
                    ttag = np.array(([tvecs[0][0][0]], [tvecs[0][0][1]], [tvecs[0][0][2]], [1]))
                    coords = Mcalibinv * ttag
                    #aruco.drawAxis(img, cameraMatrix, distcoeff, rvecs, tvecs, 0.1);
                    print(coords)


def main():
    cap = cv2.VideoCapture(0)
    cap.set(3, 1920)
    cap.set(4, 1080)

    Minv = 0

    for i in range(100):
        success, img = cap.read()
        Minv = calibrationArucoMarkers(img)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        time.sleep(0.1)
    calibration = True

    print(calibration)

    while True:
        success, img = cap.read()
        findArucoMarkers(img, Minv)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
