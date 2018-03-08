from time import sleep
import TOFSensors as TOFSensors
import SRF10_rangefinder as SRF10

import Engine
import Servos
import time

import atexit

SERVO_MIN = 600  # Min pulse length out of 4096
SERVO_MAX = 1200  # Max pulse length out of 4096

def stop_at_exit(engine):
    engine.stop_all_wheels()

def main():
    sensors = TOFSensors.TOFSensors()
    engine = Engine.Engine()
    servos = Servos.Servos()
    atexit.register(stop_at_exit, engine)

    engine.move_all_wheels_forward(50)
    servos.both_servos_down()
    servos.front_servo_forward()
    time.sleep(1)
    engine.move_all_wheels_backward(50)
    servos.both_servos_forward()
    time.sleep(1)
    engine.stop_all_wheels()
    servos.both_servos_down()

    rf = SRF10.SRF10()


    while (1):
        rf.run()
        sensors.run()
        print("State TOF Right: {}   State TOF Left: {} ".format(sensors.state_right_sensor.name,
                                                                 sensors.state_left_sensor.name))

        print("State RF: {}".format(rf.srf10_state.name))

        time.sleep(0.2)

if __name__ == '__main__':
    main()
