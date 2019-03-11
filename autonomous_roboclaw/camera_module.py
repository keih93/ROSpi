from picamera.array import PiRGBArray
from picamera import PiCamera
import time
from enum import Enum

import sys

sys.path.append('/usr/local/lib/python3.5/site-packages')

import cv2
import argparse
import numpy as np

class Direction(Enum):
    FORWARD = 0
    LEFT = 1
    RIGHT = 2
    STOP = 3
    
class CameraModule:
    
    camera = None
    rawCapture = None
    
    
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
        self.camera.rotation = 180
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.v1_min, self.v2_min, self.v3_min, self.v1_max, self.v2_max, self.v3_max = 20, 70, 110, 85, 255, 195 # yellow ball
        # blue cube: 20, 70, 110, 135, 255, 195
        # Orange ball: 9, 130, 110, 13, 255, 255
        time.sleep(0.1)
    
    
    def getDirection( self ):
        self.camera.capture(self.rawCapture, format="bgr")
        self.image = self.rawCapture.array
        frame_to_thresh = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(frame_to_thresh, (self.v1_min, self.v2_min, self.v3_min), (self.v1_max, self.v2_max, self.v3_max))
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        self.rawCapture.truncate(0)
        #print (len(cnts))
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            # only proceed if the radius meets a minimum size
            if radius > 7:
                if center[0] > 400:
                    print ("RIGHT")
                    return Direction.RIGHT
                elif center[0] < 240:
                    print ("LEFT")
                    return Direction.LEFT
                elif 240 <= center[0] <= 400:
                    print ("FORWARD")
                    return Direction.FORWARD
        print ("STOP")        
        return Direction.STOP
    
        
    
