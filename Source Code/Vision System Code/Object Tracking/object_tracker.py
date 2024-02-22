import cv2
import cv2.aruco as aruco
import numpy as np
from gpiozero import AngularServo
import math
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

marker_size = 28 #30

# Load camera calibration parameters
with open('camera_cal.npy', 'rb') as f:
    camera_matrix = np.load(f)
    camera_distortion = np.load(f)

aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)

print("Starting")
def findArucoMarkers(img, markerSize=28, totalMarkers=1, draw=True):
    arucoDict = aruco.getPredefinedDictionary(aruco.DICT_4X4_250)
    arucoParam = aruco.DetectorParameters_create()
    bbox, ids, rejected = aruco.detectMarkers(img, arucoDict, parameters=arucoParam)
    
    if draw:
        aruco.drawDetectedMarkers(img,bbox)
    return bbox, ids, rejected



def getDesired(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Get aruco
    bbox, ids, rejected = findArucoMarkers(img, markerSize=28, totalMarkers=1, draw=True)
    
    if np.any(ids == None):
        ret = 0
        centre = None
    else:
        bboxtl = bbox[0][0][0][0],bbox[0][0][0][1]
        bboxbr = bbox[0][0][2][0],bbox[0][0][2][1]

        centre = getCentre(bboxtl,bboxbr)
        ret = 1
        #print(centre)
    return centre, ret

class arucoMarker():
    def __init__(self):
        self.bboxtl = None
        self.bboxbr = None
        self.centre = None
    
    def getCentre(bboxtl,bboxbr):
        centre = int((bboxtl[0]+bboxbr[0])/2), int((bboxtl[1]+bboxbr[1])/2)
        #print(centre)
        return centre
    
def getArucos(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("image",img)
    #cv2.waitKey(1)
    # Get aruco
    arucos = list()
    bboxs, ids, rejected = findArucoMarkers(img, markerSize=28, totalMarkers=1, draw=True)
    
    if np.any(ids == None):
        ret = 0
    else:
        for bbox in bboxs:
            aruco = arucoMarker()
            aruco.bboxtl = bbox[0][0][0],bbox[0][0][1]
            aruco.bboxbr = bbox[0][2][0],bbox[0][2][1]
            aruco.centre = arucoMarker.getCentre(aruco.bboxtl,aruco.bboxbr)
            
            arucos.append(aruco)
        
        ret = 1
    return arucos, ret

def getArucoDistance(frame):
    ret, frame = vid.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejected = aruco.detectMarkers(gray_frame, aruco_dict, camera_matrix, camera_distortion)
    
    #print(ids)
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners)  # Draw a box around all the detected markers
        rvec_list_all, tvec_list_all, _objPoints = aruco.estimatePoseSingleMarkers(corners, marker_size, camera_matrix, camera_distortion)

        rvec = rvec_list_all[0][0]
        tvec = tvec_list_all[0][0]
        
        #print("rvec",rvec)
        #print("tvec",tvec)
        
        rvec_flipped = rvec * -1
        tvec_flipped = tvec * -1
        rotation_matrix, jacobian = cv2.Rodrigues(rvec_flipped)
        realworld_tvec = np.dot(rotation_matrix, tvec_flipped)
        
        print("Rotation_matrix",rotation_matrix)
        

        aruco.drawAxis(frame, camera_matrix, camera_distortion, rvec, tvec, 100)

        # Print X, Y, Z coordinates at the edges with unit (mm)
        tvec_str = "x=%4.0f mm y=%4.0f mm z=%4.0f mm" % (tvec[0], tvec[1], tvec[2])
        #cv2.putText(frame, tvec_str, (20, 460), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv2.LINE_AA)

        # Print X, Y, Z coordinates at the edges with unit (mm)
        font_size = 1.5
        #x_str = "X: %4.0f mm" % tvec[0]
        #y_str = "Y: %4.0f mm" % tvec[1]
        #z_str = "Z: %4.0f mm" % tvec[2]
        x_str = "X: %4.1f cm" % (tvec[0] / 10)
        y_str = "Y: %4.1f cm" % (tvec[1] / 10)
        z_str = "Z: %4.1f cm" % (tvec[2] / 10)

        cv2.putText(frame, x_str, (20, 40), cv2.FONT_HERSHEY_PLAIN, font_size, (255, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, y_str, (20, 80), cv2.FONT_HERSHEY_PLAIN, font_size, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(frame, z_str, (20, 120), cv2.FONT_HERSHEY_PLAIN, font_size, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    
    return 
    
def getAdjustment(windowMax, x):
    normalised_adjustment = x/windowMax - 0.5
    adjustment_magnitude = abs(round(normalised_adjustment,1))

    if normalised_adjustment>0:
        adjustment_direction = -1
    else:
        adjustment_direction = 1
        
    return adjustment_magnitude, adjustment_direction

def rescale_frame(frame, percent):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    #print("width",width)
    #print("height",height)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

vid = cv2.VideoCapture(0)
print("Video started")


# Initialise servos
pigpio_factory = PiGPIOFactory()

servo1 = AngularServo(12, pin_factory= pigpio_factory)
servo2 = AngularServo(13, pin_factory= pigpio_factory)
servo1_now = -45
servo2_now = 0
servo1.angle = servo1_now
servo2.angle = servo2_now
sleep(2)
print("Initialised servos.")

# Constants
cx = -1 #-1 # Have to change sign because this servo rotates in the wrong direction
cy = 1 # 1

Kp = 9 # 80 50 30 10 9 25 20
Kd = 4.3 #10 7 10 4 6 5 6

while(True):
    # Get image
    ret, img = vid.read()
    img = rescale_frame(img,100) #50
    window = img.shape
    
    # Get arucos
    arucos, ret = getArucos(img)
    getArucoDistance(img)
    if ret ==0:
        pass
    else:
            
        # Calculate AB (pixel error)
        A = (0,0)
        B = arucos[0].centre
        
        # show image
        #cv2.imshow("image",img)
        #cv2.waitKey(1)
        
        # Get adjustment
        xmag, xdir = getAdjustment(window[0],B[1])
        ymag, ydir = getAdjustment(window[1],B[0])

        if xmag!=None:
            
            # Proportional
            adj_Kpx = cx*Kp*xdir*xmag
            adj_Kpy = cy*Kp*ydir*ymag
            
            #Derivative
            xmag_old = xmag
            ymag_old = ymag
            
            adj_Kdx = cx*Kd*xdir*(xmag-xmag_old)
            adj_Kdy = cy*Kd*ydir*(ymag-ymag_old)
                        
            #adustment
            adjustment_x = adj_Kpx + adj_Kdx
            adjustment_y = adj_Kpy + adj_Kdy
            #servo
            servo1_now = servo1_now + adjustment_x
            servo2_now = servo2_now + adjustment_y
            
            # Reset line of sight if instructed to look out of bounds            
            if (servo1_now>90 or servo1_now<-90):
                servo1_now = 0
            if (servo2_now>90 or servo2_now<-90):
                servo2_now = 0

            servo1.angle = servo1_now
            servo2.angle = servo2_now
            sleep(0.00001)

         
        xmag = 0
        xdir = 0
        ymag = 0
        ydir = 0
        
vid.release()
cv2.destroyAllWindows()