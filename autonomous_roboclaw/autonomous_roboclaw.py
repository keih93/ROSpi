# -*- coding: utf-8 -*-
import TOFSensors

import Engine
import camera_module
from camera_module import Direction
from TOFSensors import State
import time

import atexit


def stop_at_exit(engine):
    """
    Stops all wheels when exiting program.
    :param engine:
    :return:
    """
    engine.stop_all_wheels()


def main():
    """
    Main method of the project. Starts with an init procedure and calls the functions of the used sensors in an
    infinite loop. Waits a short time after one loop step.
    :return:
    """
    # Create objects for each used sensor or actuator
    sensors = TOFSensors.TOFSensors()
    camera = camera_module.CameraModule()
    engine = Engine.Engine()
    engine.stop_all_wheels()
    atexit.register(stop_at_exit, engine)
    
    # Short init phase where wheels are rotating backwards and forwards and servos moving up and down.
    engine.move_all_wheels_forward(40)
   
    time.sleep(1)
    engine.move_all_wheels_backward(40)
    time.sleep(1)
    engine.stop_all_wheels()
    

    #TODO Messwerte mitteln
    #TODO Code etwas kommentieren
    #TODO evtl. setup.py einfuegen
    #TODO Screenshot von der Projektstruktur

    while (1):
        sensors.run()
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
    main()
