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
    
class Position(Enum):
    TOO_HIGH = 1
    CENTER = 0
    TOO_LOW = -1
    
    
class Target(object):
    """
    Struct class holding object info:

     + HSV color signatures of known objects
     + ((..HSV mins..), (..HSV maxs..)) suitable structure for use with cv2.inRange()
     + minimum size in camera
     + name
    """

    def __init__(self, min, max, rad, name):
        self.min_hsv = min
        self.max_hsv = max
        self.min_radius = rad
        self.name = name
        

class CameraModule:
    
    showImg = False
    camera = None
    rawCapture = None
    image = None
    drawHelpLines = True
    limit_left = 0.4
    limit_right = 1 - limit_left
    limit_bottom = 0.4
    limit_top = 1 - limit_bottom
    
    obj_yellow_ball = Target((20, 70, 60), (35, 255, 255), 14, "Yellow Ball")
    obj_blue_cube = Target((20, 70, 110), (135, 255, 195), 8, "Blue Cube")
    obj_orange_ball = Target((9, 130, 110), (13, 255, 255), 10, "Orange Ball")
    
    resolution = (640, 480)
    
    
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = CameraModule.resolution
        self.camera.framerate = 32
        self.camera.rotation = 180
        self.image = None
        self.objectIsFresh = False
        self.rawCapture = PiRGBArray(self.camera, size=CameraModule.resolution)
        self.setTarget(CameraModule.obj_yellow_ball)
        time.sleep(0.1)
        
    def setTarget(self, t):
        self.target = t
        print("Camera: Looking for " + self.target.name)
        
    def _fetchImage(self):
        self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
        self.image = self.rawCapture.array
      
    
    def _draw(self, ob, center):
        ((x, y), radius) = ob
        center = (int(center[0]), int(center[1]))
        if self.showImg:
            cv2.circle(self.image, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(self.image, center, 3, (0, 0, 255), -1)
            cv2.putText(self.image,"("+str(center[0])+","+str(center[1])+")",
                        (center[0]+10,center[1]+15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
            lineThickness = 1
            if self.drawHelpLines:
                y1Coor = (int)(CameraModule.resolution[1] * self.limit_top)
                y2Coor = (int)(CameraModule.resolution[1] * self.limit_bottom)
                x1Coor = (int)(CameraModule.resolution[0] * self.limit_left)
                x2Coor = (int)(CameraModule.resolution[0] * self.limit_right)
                
                cv2.line(self.image, (0,y1Coor), (640,y1Coor), (0,255,255), lineThickness)
                cv2.line(self.image, (0,y2Coor), (640,y2Coor), (0,255,255), lineThickness)
                cv2.line(self.image, (x1Coor,0), (x1Coor,480), (0,255,255), lineThickness)
                cv2.line(self.image, (x2Coor,0), (x2Coor,480), (0,255,255), lineThickness)
        
    def _find_object(self):
        """
        Find the current target object in the image.
        """
        self._fetchImage()
        frame_to_thresh = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(frame_to_thresh, self.target.min_hsv, self.target.max_hsv)
        kernel = np.ones((5,5),np.uint8)
        mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        self.rawCapture.truncate(0)
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            return (cv2.minEnclosingCircle(c), cv2.moments(c))
        return None, None

    def getPosition(self):
        """
        Get the normalized position of current target object in the image.
        
        :returns (x,y) tuple of x-y-position, or None if object not found.
        """
        
        ob, M = self._find_object()
        result = None
        if ob:
            ((x, y), radius) = ob
            # only proceed if the radius meets a minimum size
            if radius > self.target.min_radius:
                center = ((M["m10"] / M["m00"]), (M["m01"] / M["m00"]))
                self._draw(ob, center)
                result = (center[0] / CameraModule.resolution[0], center[1] / CameraModule.resolution[1])
        if self.showImg:
            cv2.imshow("Original", self.image)
            cv2.waitKey(1)
        return result
    
    
    def getDirection(self):
        """
        Find the object, get its position and translate that to a direction.
        """
        center = self.getPosition()
        if center:
            if center[0] > self.limit_right:
                print ("RIGHT")
                return Direction.RIGHT
            elif center[0] < self.limit_left:
                print ("LEFT")
                return Direction.LEFT
            else:
                print ("FORWARD")
                return Direction.FORWARD
        else:
            print ("STOP")        
            return Direction.STOP
        
    def getPositionOfObject(self, center = None):
        """
        Finds the sector of the camera image in which the center of the object was found.
        9 sectors in the image, 10th sector: object center not found in image
        """
        if not center:
            center = self.getPosition()
            
        if center:
            if center[0] > self.limit_right:
                posX = Position.TOO_HIGH
            elif center[0] < self.limit_left:
                posX = Position.TOO_LOW
            else:
                posX = Position.CENTER
            #note: screen coordinate system (y axis points downward)
            if center[1] > self.limit_top:
                return (posX, Position.TOO_LOW)
            elif center[1] < self.limit_bottom:
                return (posX, Position.TOO_HIGH)
            else:
                return (posX, Position.CENTER)
        else:
           return None
        
    
