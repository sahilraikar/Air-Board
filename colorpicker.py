import cv2
import numpy as np

def empty():
    pass

cap = cv2.VideoCapture(0)  # 0 indicates the webcam of the laptop  1 indicates the external webcam
cap.set(3, 480)  # id 3 = width for cap
cap.set(4, 240)  # id 4 = height for cap
cap.set(10, 100)  # id 10 is used for brightness and 100 is the value of brightness

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640, 240)
cv2.createTrackbar("Hue Min", "Trackbars", 0, 179, empty)  # max value of hue in open cv is 179 in general it is 360
cv2.createTrackbar("Hue Max", "Trackbars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "Trackbars", 255, 255, empty)
cv2.createTrackbar("Val Min", "Trackbars", 0, 255, empty)
cv2.createTrackbar("Val Max", "Trackbars", 255, 255, empty)

while True:
    success, img = cap.read()
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min", "Trackbars")
    h_max = cv2.getTrackbarPos("Hue Max", "Trackbars")
    s_min = cv2.getTrackbarPos("Sat Min", "Trackbars")
    s_max = cv2.getTrackbarPos("Sat Max", "Trackbars")
    v_min = cv2.getTrackbarPos("Val Min", "Trackbars")
    v_max = cv2.getTrackbarPos("Val Max", "Trackbars")
    print(h_min, h_max, s_min, s_max, v_min, v_max)

    # Creating a mask
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    imgResult = cv2.bitwise_and(img, img, mask=mask)  # merging original image with mask image

    cv2.imshow("Video", img)
    cv2.imshow("HSV IMAGE", imgHsv)
    cv2.imshow("Mask IMAGE", mask)
    cv2.imshow("IMAGE Result", imgResult)
    if cv2.waitKey(1) & 0xFF == ord('c'):   #to stop the program input 'c'
        break