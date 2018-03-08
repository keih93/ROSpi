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
    sensors = TOFSensors.TOFSensors()
    engine = Engine.Engine()
    atexit.register(stop_at_exit, engine)
    engine.move_all_wheels_forward(80)
    sleep(1)
    engine.move_all_wheels_backward(80)
    sleep(1)
    engine.stop_all_wheels()

    rf = SRF10.SRF10()
    print ("Length of rxb: " + str(len(rf.rxb)))
    print ("Bus address : " + str(rf.bus_addr))

    while (1):
        print("Sensor left distance in mm: " + str(sensors.tof_left.get_distance()))
        print("Sensor right distance in mm: " + str(sensors.tof_right.get_distance()))
        print("USS read_range : " + str(rf.measure_and_read()))
        time.sleep(2)

    stop1 = 0
    stop2 = 0
    '''
    timing = tof.get_timing()
    if (timing < 20000):
        timing = 20000
    print("Timing %d ms" % (timing / 1000))

    while (1):
        rf.run()
        sensors.run()
        print("State TOF Right: {}   State TOF Left: {} ".format(sensors.state_right_sensor.name,
                                                                 sensors.state_left_sensor.name))

        print("State RF: {}".format(rf.srf10_state.name))

        time.sleep(1)
    '''
if __name__ == '__main__':
    main()
