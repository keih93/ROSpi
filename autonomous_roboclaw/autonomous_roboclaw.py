from time import sleep
import TOFSensors as TOFSensors
import SRF10_rangefinder as SRF10

import Engine as Engine
import time
import Adafruit_PCA9685
import atexit

# Initialization at address 0x40
pwm = Adafruit_PCA9685.PCA9685()

SERVO_MIN = 200  # Min pulse length out of 4096
SERVO_MAX = 300  # Max pulse length out of 4096


def stop_at_exit(engine):
    engine.stop_all_wheels()


def main():
    sensors = TOFSensors.TOFSensor()
    engine = Engine.Engine()
    atexit.register(stop_at_exit, engine)
    engine.move_all_wheels_forward(80)
    sleep(1)
    engine.move_all_wheels_backward(80)
    sleep(1)
    engine.stop_all_wheels()

    rf = SRF10.SRF10()

    while (1):
        rf.run()
        sensors.run()
        print("State TOF Right: {}   State TOF Left: {} ".format(sensors.state_right_sensor.name,
                                                                 sensors.state_left_sensor.name))

        print("State RF: {}".format(rf.srf10_state.name))

        time.sleep(1)

if __name__ == '__main__':
    main()
