import cv2
import numpy as np
import HandTrackModule as htm
import time
import autopy

wCam, hCam = 1280, 960
frameR = 100

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0
detctor = htm.handTracker(maxHands=1)
wScrn,hScrn = autopy.screen.size()
print(wScrn,hScrn)
while True:
    # Track hand
    success, img = cap.read()
    img = detctor.trackHands(img)
    landmark, bbox = detctor.handPointPosition(img)
    cv2.rectangle(img, (frameR, frameR), (wCam-100, hCam-350), (255, 0, 255), 1)
    # Get the index corrd:
    if len(landmark) != 0:
        x1, y1 = landmark[8][1:]
        x2, y2 = landmark[12][1:]
        fingers = detctor.fingerUp()

        # Find the screen x,y assosiated to x1,y1 and x2,y2
        if fingers[1] == 1 and fingers[2] == 0 :

            x3 = np.interp(x1,(frameR,wCam-frameR),(0,wScrn))
            y3 = np.interp(y1,(frameR, hCam-350),(0,wScrn))
            # x4, y4 = np.interp(x2,(0,wCam),(0,wScrn)), np.interp(y2,(0,wCam),(0,wScrn))
            # Mouse move:
            autopy.mouse.move(wScrn-x3,y3)
            cv2.circle(img,(x1,y1),15,(255,0,255),cv2.FILLED)
        # Click:
        if fingers[1] == 1 and fingers[2] == 1 :
            lenght,img,_ = detctor.distance(img,8,12)
            print(lenght)
            if lenght < 40:
                cv2.circle(img, (_[4], _[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # Frame:
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (15, 40), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
    # Display:
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
