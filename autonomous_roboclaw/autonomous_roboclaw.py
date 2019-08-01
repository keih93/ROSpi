#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO code is compatible with py2 and py3, but not all dependencies are installed in py3

from Engine import Engine
from camera_module import CameraModule, Direction
from TOFSensors import TOFSensors, State
from Servos import Servos

import time
import signal
import argparse


def checkSectorOfObject(camera):
    position = camera.getPositionOfObject()
    if position:
        print("PosX = " + position[0].name)
        print("PosY = " + position[1].name)
    else:
        print("Object not found")


def run_test(sleeptime):
    """Move everything once, measure everything once"""
    
    if True:  # engine test
        engine = Engine()
        print('-' * 60)
        print("Testing engine")
        print("move test: forward")
        engine.move_right_wheels_forward(0)
        time.sleep(3.0)
        print("move test backwards")
        engine.move_all_wheels_backward(40)
        time.sleep(3.0)
        print("stop all")
        engine.stop_all_wheels()
    
    if True: # servo tests
        servos = Servos()
        print('-' * 60)
        print("Testing servos")
        
        def _test_servo(s):
            """Helper subroutine"""
            print("Testing servo " + s.name)
            for x in range(s.min_val, s.max_val + 1, 10):
                #print(x)
                servos.set_servo(s, x)
                time.sleep(sleeptime)
            s.reset()
        
        servos.reset()
        for servo in servos.all_servos:
            _test_servo(servo)
    
    if True:  # camera test
        camera = CameraModule()
        print('-' * 60)
        print("Testing camera")
        camera.setTarget(camera.obj_yellow_ball)
        time.sleep(10)
        camera.setTarget(camera.obj_orange_ball)
        time.sleep(10)
        camera.setTarget(camera.obj_blue_cube)
        time.sleep(10)
        
        # TODO set dfferent target objects?
    
    if True:  # sensor tests
        sensors = TOFSensors()
        print('-' * 60)
        print("Testing sensors")
        sensors.run()
        


def run_track_object(obj):
    """Main method of WS 2018/19"""
    from tracking_module import TrackingModule
    tm = TrackingModule()
    tm.camera.setTarget(obj)
    while True:
        tm.followObject()


def run_drive():
    """Old main method of SS 2018"""
    engine = Engine()
    servos = Servos()
    camera = CameraModule()
    sensors = TOFSensors()
    
    # Short init
    print("move test: forward")
    engine.move_all_wheels_forward(40)
    time.sleep(3.0)
    print("move test backwards")
    engine.move_all_wheels_backward(40)
    time.sleep(3.0)
    print("stop all")
    engine.stop_all_wheels()

    #TODO Messwerte mitteln
    #TODO Projektstruktur dokumentieren
    
    while True:
        t = time.clock()
        print("Checking sensors")
        sensors.run()
        print("Done in {0}".format([time.clock() - t]))
        command = camera.getDirection()
        
        print("State TOF Right: {}   State TOF Left: {} ".format(sensors.state_f_right_sensor.name, sensors.state_f_left_sensor.name))
        
        if sensors.state_f_left_sensor is State.BLOCKED:
            print ("back")
            engine.move_all_wheels_backward(30)
            time.sleep(3.0)
            engine.turn_around_right()
            time.sleep(3.0)

        elif sensors.state_f_right_sensor is State.BLOCKED:
            print ("BACK")
            engine.move_all_wheels_backward(30)
            time.sleep(3.0)
            engine.turn_around_left()
            time.sleep(3.0)
        
        if(command == Direction.LEFT and sensors.state_h1_sensor is State.FREE and sensors.state_h2_sensor is State.FREE):
            engine.turn_around_left()
            time.sleep(2.2)
            engine.stop_all_wheels()
        
        elif(command == Direction.RIGHT and sensors.state_h4_sensor is State.FREE and sensors.state_h5_sensor is State.FREE):
            engine.turn_around_right()
            time.sleep(2.2)
            engine.stop_all_wheels()
        
        elif(command == Direction.FORWARD and sensors.state_h3_sensor == State.FREE):
            engine.move_all_wheels_forward()
            time.sleep(2.3)
            engine.stop_all_wheels()
            
        elif(command == Direction.STOP):
            engine.stop_all_wheels()
            time.sleep(3.0)
            engine.turn_around_right()
            time.sleep(2.8)
            engine.stop_all_wheels()
        else:
            engine.stop_all_wheels()
            time.sleep(3.0)
            engine.turn_around_right()
            time.sleep(4.0)
            engine.move_all_wheels_forward()
            time.sleep(4.0)
            engine.turn_around_left()
            time.sleep(4.0)
            engine.stop_all_wheels()


def main(args):
    """
    Main method of the project. Starts with an init procedure and calls the functions of the used sensors in an
    infinite loop. Waits a short time after one loop step.
    :return:
    """
    program = args.program
    
    # test
    if program.lower().startswith("tes"):
        print("PROGRAM: test")
        run_test(args.testtime)
    elif program.lower().startswith("tra"):
        print("PROGRAM: track")
        run_track_object(args.object)
    else:
        print("PROGRAM: drive")
        run_drive()
    

if __name__ == '__main__':
    p = argparse.ArgumentParser(description="RoboClaw runner script")
    p.add_argument("--program", "-p", default="drive", type=str, help="Which program to run")
    
    # test args
    #p.add_argument("--testtime", "-t", default=0.5, type=float, help="Time interval used in sleeps() inside the program TEST.")
    
    # track args
    #p.add_argument("--object", "-o", default="yellow", type=str, help="Object to look for in the program TRACK.")
    
    main(p.parse_args())

