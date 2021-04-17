from cv2 import cv2
import mediapipe as mp
import time
import pickle,sys
import pandas as pd
import os
os.chdir(os.path.join(os.path.split(os.path.abspath(__file__))[0],".."))

def camera():
    LReg= pickle.load(open("models/basicLR_3.pkl", 'rb'))
    cols=[]
    for i in range(1,43):
        cols.append("col-"+str(i))

    cap = cv2.VideoCapture(0)
    
    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils
    
    pTime = 0
    cTime = 0
    t_end = time.time()+30
    while time.time()<t_end:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
    
        if results.multi_hand_landmarks:
            cnt=0
            for handLms in results.multi_hand_landmarks:
                print(cnt)
                cnt=cnt+1
                data_points = []
                l=[]
                l2=[]
                for id, lm in enumerate(handLms.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    #print(id, cx, cy)
                    data_points.extend([cx,cy])
                    # if id == 4:
                    #cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                for i in range(0,42,2):
                    l.append(int(data_points[i])-int(data_points[0]))
                    l.append(int(data_points[i+1])-int(data_points[1]))
                l2.append(l)
                df = pd.DataFrame(l2, columns = cols) 
                
                #mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                try:
                    symbol = LReg.predict(df)
                    if cnt==1:
                        cv2.putText(img, str(symbol[0]), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,(55, 55, 55), 7)
                    else:
                        cv2.putText(img, str(symbol[0]), (10, 140), cv2.FONT_HERSHEY_PLAIN, 3,(55, 55, 55), 7)
                except:
                    pass
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        
    #    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,(255, 0, 255), 3)
    
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    cap.release()   