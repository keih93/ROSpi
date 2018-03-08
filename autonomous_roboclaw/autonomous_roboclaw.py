from time import sleep
import autonomous_roboclaw.TOFSensors as TOFSensors
import autonomous_roboclaw.SRF10_rangefinder as SRF10

import autonomous_roboclaw.Engine
import autonomous_roboclaw.Servos
from autonomous_roboclaw.TOFSensors import State
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

        if rf.srf10_state is State.BLOCKED:
            engine.move_all_wheels_backward(30)
            time.sleep(0.5)
            engine.stop_all_wheels()
            engine.move_left_wheels_backward(20)
            engine.move_right_wheels_forward(20)


if __name__ == '__main__':
    main()
