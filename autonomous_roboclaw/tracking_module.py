import camera_module
Position = camera_module.Position
import Servos
import math
import time
from threading import Thread


class TrackingModule:
    
    camera = camera_module.CameraModule()
    s = Servos.Servos()
    servoFace = s.servoFace
    servoHead = s.servoHead
    servoTail = s.servoTail
    lastSeenX = None
    lastSeenY = None
    moveTailForward = True
    
    def __init__(self):
        pass
    
    def followObject(self):
        def calcSpeeds():
            """Helper subroutine, using outer vars x, y, x_speed, y_speed"""
            n_x = abs(x_speed - 0.5)
            n_x *= math.log(1 + n_x) 
            
            if x is Position.TOO_HIGH:
                x_s = n_x
            elif x is Position.TOO_LOW:
                x_s = -1 * n_x
            else:
                x_s = 0
            
            n_y = abs(y_speed - 0.5)
            n_y *= math.log(1 + n_y)
            
            if y is Position.TOO_HIGH:
                y_s = -1 * n_y
            elif y is Position.TOO_LOW:
                y_s = n_y
            else:
                y_s = 0
            return x_s, y_s
        
        x_step = 100
        y_step = 40
        
        currentOffset = self.camera.getPosition() 
        currentSector = self.camera.getPositionOfObject(currentOffset)
        
        if currentSector is None or currentOffset is None:  # if no object found
            if self.lastSeenX is None or self.lastSeenY is None:  # and we have never seen it
                # go into default pose? start scanning the surrounding?
                return
            else:
                # look in the direction, we have seen the object lately
                x = self.lastSeenX
                y = self.lastSeenY
                x_speed = float(x.value / 10.0)  # search in last direction with offset +-1!
                y_speed = float(y.value / 10.0) # XXX using knowledge about enum values ...
                
        else:
            # object found
            x, y = currentSector
            x_speed, y_speed = currentOffset  # temporary, used in calcSpeeds()
            self.lastSeenX, self.lastSeenY = currentSector # save for later
            
        if x is Position.CENTER and y is Position.CENTER:
            self.moveTail()
            return
        
        x_speed, y_speed = calcSpeeds()
        
        self.servoFace.addval(x_speed * x_step)
        
        self.servoHead.addval(y_speed * y_step)
    
    def moveTail(self):
        if self.moveTailForward:
            self.servoTail.addval(20)
            if self.servoTail.val >= self.servoTail.max_val:
                self.moveTailForward = False
        else:
            self.servoTail.addval(-20)
            if self.servoTail.val <= self.servoTail.min_val:
                self.moveTailForward = True

def main():
    tm = TrackingModule()
    while True:
        tm.followObject()
        #tm.moveTail()

if __name__ == '__main__':
    main()