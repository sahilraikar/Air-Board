import cv2
import numpy as np
import math

def empty():
    pass

cap=cv2.VideoCapture(0)
cap.set(3,720)
cap.set(4,480)
cap.set(10,150)
cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars",550,70)
cv2.createTrackbar("Thickness","Trackbars",2,10,empty)
cv2.createTrackbar("Radius","Trackbars",10,100,empty)

myColor = [[143,59,0,179,255,255]]
colorVal=[[0,165,255],[0,0,255],[0,255,255],[255,0,255],[255,255,0],[255,255,255]]
myPoints=[]#x,y,colorIn
oldPoints=[0,0,1]
null=[-1,-1,1]
x2=-1
y2=-1
c=0
d=0
ch=0

def findColor(img,myColor,colorVal):
    count=0
    newPoints=[]
    global ch
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    for color in myColor:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHsv, lower, upper)
        cv2.imshow(str(color[0]),mask)
        x,y = getContours(mask)
        cv2.circle(imgRes,(x,y),10,colorVal[ch],cv2.FILLED)
        if(x>10 and x<120)and (y>10 and y<80):
            ch=1
        elif (x > 150 and x < 260) and (y > 10 and y < 80):
            ch = 2
        elif (x > 290 and x < 400) and (y > 10 and y < 80):
            ch = 3
        elif (x > 430 and x < 540) and (y > 10 and y < 80):
            ch = 4
        elif (x > 570 and x < 650) and (y > 10 and y < 80):
            ch = 5
        newPoints.append([x,y,ch])
        count+=1
    return newPoints



def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)#retieves the extreme outer contours
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area=cv2.contourArea(cnt)
        if area>100:
            cv2.drawContours(imgRes, cnt, -1, (255, 0, 0),3)  # draws the contours by taking contours in for loop(cnt) , -1 indicates index in this case since -1 means all contours
            peri=cv2.arcLength(cnt,True)#true indicates the shape is closed
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)#0.02*peri is the resolution & true indicates the shape is closed
            x,y,w,h=cv2.boundingRect(approx)
        else:
            pass
    return x+w//2,y

def draw(myPoints,x2,y2,colorVal,oldPoints,Thickness):
    for p1 in myPoints:
        if (x2==-1 and y2==-1):
            x2, y2 =p1[0],p1[1]
            oldPoints=p1
        elif(p1==null):
            x2,y2=-1,-1
        else:
            cv2.line(imgRes,(p1[0],p1[1]),(x2,y2),colorVal[p1[2]],Thickness)
            cv2.line(canvas, (p1[0], p1[1]), (x2, y2), colorVal[p1[2]], Thickness)
            x2, y2=p1[0],p1[1]
            oldPoints=p1
    #print("old point = ",oldPoints)
    return oldPoints

while True:
    Success,img=cap.read()
    img=cv2.resize(img,(720,480))
    canvas = np.zeros((480, 720, 3), np.uint8)
    canvas.fill(255)
    imgRes=img.copy()
    Thickness = cv2.getTrackbarPos("Thickness", "Trackbars")
    Radius = cv2.getTrackbarPos("Radius", "Trackbars")
    newPoints=findColor(img,myColor,colorVal)
    d=0
    if len(newPoints)!=0:
        for newP in newPoints:
            if(newP[0]!=0 and newP[1]!=0 and newP[2]!=5) and newP not in myPoints:
                if(oldPoints[0]!=0 and oldPoints[1]!=0):
                    #print("newP[0] = ",newP[0])
                    #print("newP[1] = ", newP[1])
                    #print("old[0] = ", oldPoints[0])
                    #print("old[1] = ", oldPoints[1])
                    #print("oldPoints = ",oldPoints)
                    d = ((int(newP[0]) - int(oldPoints[0])) * (int(newP[0]) - int(oldPoints[0]))) + ((int(newP[1]) - int(oldPoints[1])) * (int(newP[1]) - int(oldPoints[1])))
                    d=math.sqrt(d)
                if(d>50):
                    myPoints.append(null)
                #print("Distance = ", d)
                #print('newPoints=',newP)
                myPoints.append(newP)
            elif(newP[0]!=0 and newP[1]!=0 and newP[2]==5):
                for p in myPoints:
                    if((p[0]-newP[0])*(p[0]-newP[0])+(p[1]-newP[1])*(p[1]-newP[1])<math.pow(Radius,2)):
                        index=myPoints.index(p)
                        cv2.circle(canvas,(p[0],p[1]),Radius,(255,255,255))
                        myPoints[index]=null


    if len(myPoints) != 0 :
        oldPoints=draw(myPoints,x2,y2,colorVal,oldPoints,Thickness)
    cv2.rectangle(imgRes, (10, 10), (120, 80), (0, 0, 255), cv2.FILLED)
    cv2.rectangle(imgRes, (150, 10), (260, 80), (0, 255, 255), cv2.FILLED)
    cv2.rectangle(imgRes, (290, 10), (400, 80), (255, 0, 255), cv2.FILLED)
    cv2.rectangle(imgRes, (430, 10), (540, 80), (255, 255, 0), cv2.FILLED)
    cv2.rectangle(imgRes, (570, 10), (650, 80), (255, 255, 255), cv2.FILLED)
    imgRes = cv2.flip(imgRes, 1)
    canvasRes=cv2.flip(canvas,1)
    cv2.imshow("Result", imgRes)
    cv2.imshow("canvas", canvasRes)
    if cv2.waitKey(1)& 0xFF==ord('e'):
        myPoints.clear()
        oldPoints=[0,0,1]
        canvas.fill(255)
        ch=0
    if cv2.waitKey(1)& 0xFF==ord('c'):
        #print(myPoints)
        exit(0)