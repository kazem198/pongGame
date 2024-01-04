import cv2
import numpy as np
import cvzone
from cvzone.HandTrackingModule import HandDetector
from cvzone.Utils import rotateImage

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

imgBackground = cv2.imread("Resources/Background.png")
imgBall = cv2.imread("Resources/Ball.png", cv2.IMREAD_UNCHANGED)
imgbat1 = cv2.imread("Resources/bat1.png", cv2.IMREAD_UNCHANGED)
imgbat2 = cv2.imread("Resources/bat2.png", cv2.IMREAD_UNCHANGED)
imgGameOver = cv2.imread("Resources/gameOver.png")

detector = HandDetector(maxHands=2, detectionCon=0.8)

posBat1 = [60, 100]  # left
posBat2 = [1195, 100]  # right
speedX = 15
speedY = 15
ballPos = [100, 100]
scoreRight = 0
scoreLeft = 0
gameOver = False


while True:
    _, img = cap.read()
    img = cv2.flip(img, 1)
    if gameOver == False:

        hands, img = detector.findHands(img, draw=True, flipType=False)

        img = cv2.addWeighted(img, 0.2, imgBackground, 0.8, 0)
        img = cvzone.overlayPNG(img, imgbat1, posBat1)
        img = cvzone.overlayPNG(img, imgbat2, posBat2)

        if hands:

            for hand in hands:
                x, y, w, h = hand["bbox"]

                if hand["type"] == "Right":
                    y1 = np.clip(y, 80, 500)

                    posBat2[1] = y1-65

                else:
                    y1 = np.clip(y, 80, 500)
                    posBat1[1] = y1-65

        ballPos[0] += speedX
        ballPos[1] += speedY

        if (ballPos[1] > 500 or ballPos[1] < 10):
            speedY = -speedY
    #     right bat
        if ballPos[0] > 1150 and posBat2[1] < ballPos[1] < posBat2[1]+130:
            speedX = -speedX
            ballPos[0] -= 50
            scoreRight += 1

        #  left ball
        elif ballPos[0] < 70 and posBat1[1] < ballPos[1] < posBat1[1]+130:
            speedX = -speedX
            ballPos[0] += 50
            scoreLeft += 1

        cvzone.overlayPNG(img, imgBall, ballPos)

        cvzone.putTextRect(img, str(scoreRight), (1200, 680))
        cvzone.putTextRect(img, str(scoreLeft), (80, 680), colorR=(0, 255, 0))

        if ballPos[0] < 50 or ballPos[0] > 1200:
            gameOver = True

    else:
        img = imgGameOver
        cvzone.putTextRect(img, str(scoreRight), (660, 330))
        cvzone.putTextRect(img, str(scoreLeft),
                           (580, 330), colorR=(0, 255, 0))

    cv2.imshow("img", img)
    # cv2.imshow("imgball", imgRotated60KeepSize)
    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break
    elif key == ord("r"):
        ballPos = [100, 100]
        scoreRight = 0
        scoreLeft = 0
        gameOver = False
        speedX = 15
        speedY = 15
