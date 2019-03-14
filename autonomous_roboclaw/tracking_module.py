import camera_module
Position = camera_module.Position
import Servos
import math

class TrackingModule:
    
    camera = camera_module.CameraModule()
    s = Servos.Servos()
    servoFace = s.servoFace
    servoHead = s.servoHead
    servoTail = s.servoTail
    lastSeenX = None
    lastSeenY = None
    tailForward = True
    
    def __init__(self):
        pass

    def followObject(self):
        def calcSpeeds():
            """Helper subroutine"""
            n_x = abs(x_speed - 0.5)
            n_x *= math.log(1 + n_x)  #abs(x_speed - 0.5)**2  # TODO simple x^2-function is not ideal here!
            
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
        
        x_step = 200
        y_step = 200
        
        currentOffset = self.camera.getPosition() 
        currentSector = self.camera.getPositionOfObject(currentOffset)
        
        if currentSector is None or currentOffset is None:
            if self.lastSeenX is None or self.lastSeenY is None:
                # TODO go into default pose, or start scanning the surrounding
                return
            x = self.lastSeenX
            y = self.lastSeenY
            x_speed = (float) (x.value / 10)  # search in last direction with offset +-1!
            y_speed = (float) (y.value / 10) # XXX using knowledge about enum values ...
        else:
            x, y = currentSector
            x_speed, y_speed = currentOffset
            self.lastSeenX, self.lastSeenY = currentSector # save for later
            self.moveTail()
        
        if x is Position.CENTER and y is Position.CENTER:
            # nothing to do, we are looking at the object
            return
        
        x_speed, y_speed = calcSpeeds()
        
        self.servoFace.addval(x_speed * x_step)
        
        self.servoHead.addval(y_speed * y_step)

    def moveTail(self):
        if self.tailForward:
            self.servoTail.addval(20)
            self.tailForward = False
        else:
            self.servoTail.addval(-20)
            self.tailForward = True
        
            
def main():
    tm = TrackingModule()
    while True:
        tm.followObject()

if __name__ == '__main__':
    main()