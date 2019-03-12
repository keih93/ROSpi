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

class CameraModule:
    
    camera = None
    rawCapture = None
    limit_left = 0.375
    limit_right = 1 - limit_left
    limit_bottom = 0.375
    limit_top = 1 - limit_bottom
    
    
    # HSV color signatures of known objects
    # ((..HSV mins..), (..HSV maxs..)) suitable structure for use with cv2.inRange()
    obj_yellow_ball = ((20, 70, 110), (85, 255, 195), 7)
    obj_blue_cube = ((20, 70, 110), (135, 255, 195), 4)
    obj_orange_ball = ((9, 130, 110), (13, 255, 255), 5)
    
    resolution = (640, 480)
    
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = CameraModule.resolution
        self.camera.framerate = 32
        self.camera.rotation = 180
        self.rawCapture = PiRGBArray(self.camera, size=CameraModule.resolution)
        self.target = CameraModule.obj_yellow_ball
        time.sleep(0.1)
        
    def _find_object(self):
        """
        Find the current target object in the image.
        """
        self.camera.capture(self.rawCapture, format="bgr")
        self.image = self.rawCapture.array
        frame_to_thresh = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(frame_to_thresh, self.target[0], self.target[1])
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
        Get the normalized position of our target object in the image.
        """
        ob, M = self._find_object()
        if ob:
            ((x, y), radius) = ob
            # only proceed if the radius meets a minimum size
            if radius > self.target[2]:
                center = ((M["m10"] / M["m00"]), (M["m01"] / M["m00"]))
                return (center[0] / CameraModule.resolution[0], center[1] / CameraModule.resolution[1])
        return None
    
    
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
        
    def getPositionOfObject(self):
        """
        Finds the sector of the camera image in which the center of the object was found.
        9 sectors in the image, 10th sector: object center not found in image
        """
        
        center = self.getPosition()
        if center:
            print("Coordinates: %s" % (center,))
            if center[0] > self.limit_right:
                posX = Position.TOO_HIGH
            elif center[0] < self.limit_left:
                posX = Position.TOO_LOW
            else:
                posX = Position.CENTER
            #note: screen ccordinate system (y axis points downward)
            if center[1] > self.limit_top:
                return (posX, Position.TOO_LOW)
            elif center[1] < self.limit_bottom:
                return (posX, Position.TOO_HIGH)
            else:
                return (posX, Position.CENTER)
        else:
           return None
        
    
