import cv2
import numpy as np
import dlib
from math import hypot
def nothing(x):
    pass
cap = cv2.VideoCapture(0)
cv2.namedWindow("Trackbars")
cv2.createTrackbar("th", "Trackbars", 99, 255, nothing)
cv2.createTrackbar("brightness", "Trackbars", 110, 255, nothing)
cv2.createTrackbar("contrast", "Trackbars", 89, 130, nothing)
#next function is to detect brightness and contrast
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0): 
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow
        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()
    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)
    return buf
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
center=None
blinking_times=0
xx=yy=0
timer=0
def midpoint(p1 ,p2):
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)
#............................................................................................................
while True:
    _, frame = cap.read()
    frame= cv2.flip(frame, 1)
    #we use next function if we use video saved before
    #frame=cv2.resize(frame,None,fx=.25,fy=.25)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    num_faces=len(faces)
    th = cv2.getTrackbarPos("th", "Trackbars")
    brightness = cv2.getTrackbarPos("brightness", "Trackbars")
    contrast = cv2.getTrackbarPos("contrast", "Trackbars")

    fac=[]
    areaa=[]
    for face in faces:
        fac.append(face)
        areaa.append(face.area())
        indec=areaa.index(max(areaa))
        facy=fac[indec]
        if len(fac)==num_faces:
            #print(fac,areaa,facy)
            x_left, y_top = facy.left(), facy.top()
            x_right, y_bottom = facy.right(), facy.bottom()
            #cv2.rectangle(frame, (x_left,y_top ), (x_right, y_bottom ), (0, 255, 0), 2)
            landmarks = predictor(gray, facy)
            #.....................................................................................................
            #RIGHT EYE PROCESSING
            
            img=frame[landmarks.part(44).y+2:landmarks.part(46).y-2,landmarks.part(42).x+3:landmarks.part(45).x-3]
            if img is not None :
                pass
            if img.shape[0] <1: 
                break
            img=cv2.resize(img,None,fx=10,fy=10)
            img=apply_brightness_contrast(img, brightness , contrast )
            img_length=img.shape[0]
            img_width=img.shape[1]
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #gray_img = cv2.equalizeHist(gray_img)
            gray_img = cv2.GaussianBlur(gray_img, (9, 9), 0)
            _, threshold = cv2.threshold(gray_img, th, 255, cv2.THRESH_BINARY_INV)
            contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)
            for cnt in contours:
                area=cv2.contourArea(cnt)
                if area>=7000:
                    (x,y),raduis=cv2.minEnclosingCircle(cnt)
                    center=(int(x),int(y))
                    cv2.circle(img,center,int(raduis/5),(0,255,255),2)
                    cv2.drawContours(img, [cnt], -1, (0, 255, 0), 3)        
            stp_x=int(img_width/3)
            cv2.imshow("img", img)
            cv2.imshow("th", threshold)
            #...................................................................................................
            #left eye
            left_point_l = (landmarks.part(36).x, landmarks.part(36).y)
            right_point_l = (landmarks.part(39).x, landmarks.part(39).y)
            center_top_l = midpoint(landmarks.part(37), landmarks.part(38))
            center_bottom_l = midpoint(landmarks.part(41), landmarks.part(40))
            hor_line_l = cv2.line(frame, left_point_l, right_point_l, (100, 50, 25), 1)
            ver_line_l = cv2.line(frame, center_top_l, center_bottom_l, (100, 50, 25), 1)
            
            #right eye        
            left_point_r = (landmarks.part(42).x, landmarks.part(42).y)
            right_point_r = (landmarks.part(45).x, landmarks.part(45).y)
            center_top_r= midpoint(landmarks.part(43), landmarks.part(44))
            center_bottom_r = midpoint(landmarks.part(47), landmarks.part(46))
            hor_line1_r = cv2.line(frame, left_point_r, right_point_r, (100, 50, 25), 1)
            ver_line1_r= cv2.line(frame, center_top_r, center_bottom_r, (100, 50, 25), 1)
            
            #left eye ratio to detect blinking
            hor_line_lenght_l = hypot((left_point_l[0] - right_point_l[0]), (left_point_l[1] - right_point_l[1]))
            ver_line_lenght_l= hypot((center_top_l[0] - center_bottom_l[0]), (center_top_l[1] - center_bottom_l[1]))
            ratio_l= hor_line_lenght_l/ ver_line_lenght_l
            
            #right eye ratio to detect blinking
            hor_line_lenght_r = hypot((left_point_r[0] - right_point_r[0]), (left_point_r[1] - right_point_r[1]))
            ver_line_lenght_r = hypot((center_top_r[0] - center_bottom_r[0]), (center_top_r[1] - center_bottom_r[1]))
            ratio_r = hor_line_lenght_r / ver_line_lenght_r
            
            #blinking condition
            if center is  None:
                break
            
            if ratio_r<5 and ratio_l<5 :
                yy=1
                xx=0
                timer=0
            elif ratio_r>=5 and ratio_l>=5 :
                xx=1
                timer=timer+1
            if xx==1 and yy==1 and timer >= 6:
                blinking_times=blinking_times+1
                xx=yy=0
              
            if blinking_times%2==1 :
                if center[0] > 2*stp_x: #or > 220
                    cv2.putText(frame,"Right",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),5)
                    #print("right")
                elif center[0]< stp_x: #or < 109
                    cv2.putText(frame,"Left",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),5)
                    #print("left")
                elif 2*stp_x >center[0]> stp_x:
                    cv2.putText(frame,"Center",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),5)
                    #print("center")
            elif blinking_times%2==0:
                cv2.putText(frame,"Stop",(50,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),5)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()
