import camera_module
Position = camera_module.Position
import Servos
import math
import time
import Engine
import TOFSensors
from threading import Thread
from enum import Enum


class State(Enum):
    FREE = 0
    BLOCKED = 1
    ERROR = 2

class TrackingModule:
    tof_h1 = None
    tof_h2 = None
    tof_h3 = None
    tof_h4 = None
    tof_h5 = None
    tof_f_right = None
    tof_f_left = None
    state_f_left = State.FREE
    state_f_right = State.FREE
        
    engine = Engine.Engine()
    tof = TOFSensors.TOFSensors()
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

    def followObject(self, withHead=True):
        # ------------------------
        # withHead:
        # differ in vertical movement between movement with head and movement by wheels
        # ------------------------
        
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

        # differ in vertical movement between movement with head and movement by wheels

        if withHead:
                self.servoFace.addval(x_speed * x_step)			
        else:
            if (x_speed * x_step) > 0:
                speed = int(x_speed * 300)
                if x_speed < 0.05:  
                    speed = 20
                self.engine.turn_around_right(speed)
            elif (x_speed * x_step) < 0:
                speed = int(-x_speed * 300)
                if x_speed > -0.05:
                    speed = 20
                self.engine.turn_around_left(speed)

        # always move the Head horizontally. 
        self.servoHead.addval(y_speed * y_step * 3)
        
    
    def moveTail(self):
        if self.moveTailForward:
            self.servoTail.addval(80)
            if self.servoTail.val >= self.servoTail.max_val:
                self.moveTailForward = False
        else:
            self.servoTail.addval(-80)
            if self.servoTail.val <= self.servoTail.min_val:
                self.moveTailForward = True
     
        #Get TOF Sensor Data
        distance_h2_sensor = self.tof.tof_h2.get_distance()
        distance_h3_sensor = self.tof.tof_h3.get_distance()
        distance_h4_sensor = self.tof.tof_h4.get_distance()
        distance_f_right_sensor = self.tof.tof_f_right.get_distance()
        distance_f_left_sensor = self.tof.tof_f_left.get_distance()
        
        #Set States if their is no floor left
        if distance_f_right_sensor > 300:
            self.state_f_right = State.BLOCKED

        else:
            self.state_f_right = State.FREE

        if distance_f_left_sensor > 300:
            self.state_f_left = State.BLOCKED

        else:
            self.state_f_left = State.FREE
        
        #print("Distance f_left sensor: {} , Distance f_right sensor: {}, State Left {}, State Right {}".format(str(distance_f_right_sensor),
         #                                                                      str(distance_f_left_sensor), str(self.state_f_left),
          #                                                                                                     str(self.state_f_right)))
        #print("h2: {} , h3: {} , h4: {}".format(str(distance_h2_sensor), str(distance_h3_sensor), str(distance_h4_sensor)))
        
        
        sum_distance = distance_h2_sensor + distance_h3_sensor + distance_h4_sensor
        
        #Drive forward if we detect the ball in front of us and if their is floor left
        if sum_distance / 3 > 200 and self.state_f_left is State.FREE and self.state_f_right is State.FREE:
            self.engine.move_all_wheels_forward(40)
        elif distance_f_right_sensor == -1 and distance_f_left_sensor == -1:
            self.engine.stop_all_wheels()
        else:
            self.engine.stop_all_wheels()
        

def main():
    tm = TrackingModule()
    while True:
        tm.followObject(False)
        #tm.moveTail()

if __name__ == '__main__':
    main()
