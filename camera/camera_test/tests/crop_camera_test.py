#Show image, video, webcam
import cv2

#webcam

#dimensions image : (longueur, hauteur) = (480, 270) ou (640,480) ou (1920, 1080)
longueur = 1920
hauteur = 1080

capture = cv2.VideoCapture(0)
capture.set(3, longueur)
capture.set(4, hauteur)
capture.set(10, 10) # 10 brightness


while True:
    success, img = capture.read() #save image in img, and tell if successful in success(true/False)
    
    cropped_image = img[int(hauteur/2)-100:hauteur-170, int(longueur/2)+50:longueur-80]
    cv2.imshow("crop camera", cropped_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        #Stops if press q
        break