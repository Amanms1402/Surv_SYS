import cv2
from cvzone.PoseModule import PoseDetector
import send

def surveillance_system():
    detector = PoseDetector()
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    l = []
    flag = True
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        imlist, bbox = detector.findPosition(img)
        if len(imlist) > 0:
            l.append(1)
        if len(l) > 50 and flag:
            flag = False
            send.send_sms()
        cv2.imshow("Surveillance Screen", img)
        q = cv2.waitKey(1)
        if q == ord('q'):
            break
    
    


