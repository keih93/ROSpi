from time import sleep
import autonomous_roboclaw.TOFSeonsors as TOFSensors
import autonomous_roboclaw.SRF10_rangefinder as SRF10

import autonomous_roboclaw.Engine as Engine
import time
import Adafruit_PCA9685
import atexit
import threading

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
    engine.move_all_wheels_forward(20)
    sleep(2)
    engine.move_all_wheels_backward(20)
    sleep(2)
    engine.stop_all_wheels()

    rf = SRF10.SRF10()

    threading._start_new_thread(rf.run())
    threading._start_new_thread(sensors.run())

    print("Length of rxb: " + str(len(rf.rxb)))
    print("Bus address : " + str(rf.bus_addr))

    while (1):
        print("State TOF Right: {}   State TOF Left: {} ".format(sensors.state_right_sensor.name,
                                                                 sensors.state_left_sensor.name))
        print("State RF: {}".format(rf.srf10_state.name))
        print("Sensor left distance in mm: " + str(sensors.tof_left.get_distance()))
        print("Sensor right distance in mm: " + str(sensors.tof_right.get_distance()))
        print("USS read_range : " + str(rf.measure_and_read()))
        time.sleep(2)


if __name__ == '__main__':
    main()
