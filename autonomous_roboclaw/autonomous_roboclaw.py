from time import sleep
import TOFSensors
import SRF02_rangefinder as SRF02

import Engine
import Servos
from TOFSensors import State
import time

import atexit

SERVO_MIN = 600  # Min pulse length out of 4096
SERVO_MAX = 1200  # Max pulse length out of 4096


def stop_at_exit(engine):
    """
    Stops all wheels when exiting program.
    :param engine:
    :return:
    """
    engine.stop_all_wheels()


def main():
    sensors = TOFSensors.TOFSensors()
    engine = Engine.Engine()
    servos = Servos.Servos()
    atexit.register(stop_at_exit, engine)

    engine.move_all_wheels_forward(40)
    servos.both_servos_down()
    servos.front_servo_forward()
    time.sleep(1)
    engine.move_all_wheels_backward(40)
    servos.both_servos_forward()
    time.sleep(1)
    engine.stop_all_wheels()
    servos.both_servos_down()

    rf = SRF02.SRF02()

    #TODO Messwerte mitteln
    #TODO Code etwas kommentieren
    #TODO evtl. setup.py einfügen
    #TODO Screenshot von der Projektstruktur
    while (1):
        rf.run()
        sensors.run()
        print("State TOF Right: {}   State TOF Left: {} ".format(sensors.state_right_sensor.name,
                                                                 sensors.state_left_sensor.name))

        print("State RF: {}".format(rf.srf02_state.name))

        if rf.srf02_state is State.BLOCKED:

            engine.turn_around_left()

        elif sensors.state_left_sensor is State.BLOCKED:
            engine.move_all_wheels_backward(30)
            time.sleep(1.5)
            engine.turn_around_right()
            time.sleep(1.5)

        elif sensors.state_right_sensor is State.BLOCKED:
            engine.move_all_wheels_backward(30)
            time.sleep(1.5)
            engine.turn_around_left()
            time.sleep(1.5)

        else:
            engine.move_all_wheels_forward(40)

        time.sleep(0.1)


if __name__ == '__main__':
    main()
