# -*- coding: utf-8 -*-
from Engine import Engine
import camera_module
Direction = camera_module.Direction
import TOFSensors
State = TOFSensors.State
from Servos import Servos

import time
import atexit
import argparse


def stop_at_exit(engine):
    """
    Stops all wheels when exiting program.
    :param engine:
    :return:
    """
    engine.stop_all_wheels()


def shake_head():
    pass

def nod_head():
    pass

def checkSectorOfObject(camera):
    position = camera.getPositionOfObject()
    if position:
        print("PosX = " + position[0].name)
        print("PosY = " + position[1].name)
    else:
        print("Object not found")

def main(testtime=0.0):
    """
    Main method of the project. Starts with an init procedure and calls the functions of the used sensors in an
    infinite loop. Waits a short time after one loop step.
    :return:
    """
    # Create objects for each used sensor or actuator
    engine = Engine()
    engine.stop_all_wheels()
    atexit.register(stop_at_exit, engine)
    
    # Short init phase where wheels are rotating backwards and forwards and
    
    servos = Servos()
    camera = camera_module.CameraModule()
    while True:
        checkSectorOfObject(camera)
        
    if testtime > 0.0:
        print("-"*60)
        servos.set_servo(Servos.SERVO_HEAD, Servos.HEAD_UP)        
        servos.set_servo(Servos.SERVO_FACE, Servos.FACE_LEFT)
        time.sleep(testtime)
        servos.set_servo(Servos.SERVO_FACE, Servos.FACE_RIGHT)
        time.sleep(testtime)
        servos.set_servo(Servos.SERVO_FACE, Servos.FACE_FORWARD)
        time.sleep(testtime)
        
        for x in range(Servos.HEAD_UP, Servos.HEAD_DOWN, 200):
            print(x)
            servos.set_servo(Servos.SERVO_HEAD, x)
            time.sleep(testtime)
        
        
        servos.set_servo(Servos.SERVO_HEAD, Servos.HEAD_UP)
        time.sleep(testtime)
        servos.set_servo(Servos.SERVO_HEAD, 0)
        time.sleep(testtime)
        
        while True:
            
            print("move test: forward")
            engine.move_all_wheels_forward(40)
            time.sleep(testtime)
            
            print("move test backwards")
            engine.move_all_wheels_backward(40)
            time.sleep(testtime)
            
            print("stop all")
            engine.stop_all_wheels()
        return # TEST DEBUG
    
    sensors = TOFSensors.TOFSensors()
   

    #TODO Messwerte mitteln, was heisst das? h1+h2/2, h2+h3/2, ... ???
    #TODO Projektstruktur dokumentieren
    
    
    while (1):
        t = time.clock()
        print("Checking sensors")
        sensors.run()
        print("Done in {0}".format([time.clock() - t]))
        command = camera.getDirection()
        #print("State TOF Right: {}   State TOF Left: {} ".format(sensors.state_f_right_sensor.name, sensors.state_f_left_sensor.name)
        
        if sensors.state_f_left_sensor is State.BLOCKED:
            print ("back")
            engine.move_all_wheels_backward(30)
            time.sleep(1.0)
            engine.turn_around_right()
            time.sleep(1.0)

        elif sensors.state_f_right_sensor is State.BLOCKED:
            print ("BACK")
            engine.move_all_wheels_backward(30)
            time.sleep(1.0)
            engine.turn_around_left()
            time.sleep(1.0)
        
        if(command == Direction.LEFT and sensors.state_h1_sensor is State.FREE and sensors.state_h2_sensor is State.FREE):
            engine.turn_around_left()
            time.sleep(0.2)
            engine.stop_all_wheels()
        
        elif(command == Direction.RIGHT and sensors.state_h4_sensor is State.FREE and sensors.state_h5_sensor is State.FREE):
            engine.turn_around_right()
            time.sleep(0.2)
            engine.stop_all_wheels()
        
        elif(command == Direction.FORWARD and sensors.state_h3_sensor == State.FREE):
            engine.move_all_wheels_forward()
            time.sleep(0.3)
            engine.stop_all_wheels()
            
        elif(command == Direction.STOP):
            engine.stop_all_wheels()
            time.sleep(1.0)
            engine.turn_around_right()
            time.sleep(0.8)
            engine.stop_all_wheels()
        else:
            engine.stop_all_wheels()
            time.sleep(1.0)
            engine.turn_around_right()
            time.sleep(2.0)
            engine.move_all_wheels_forward()
            time.sleep(2.0)
            engine.turn_around_left()
            time.sleep(2.0)
            engine.stop_all_wheels()
       
            

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument("--testtime", default=0.0, type=float)
    
    args = p.parse_args()
    
    main(args.testtime)
