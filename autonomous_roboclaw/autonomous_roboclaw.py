from time import sleep

import autonomous_roboclaw.Engine as Engine
import time
import Adafruit_PCA9685
import os
import autonomous_roboclaw.VL53L0X as VL53L0X
import atexit

# Initialization at address 0x40
pwm = Adafruit_PCA9685.PCA9685()

SERVO_MIN = 200  # Min pulse length out of 4096
SERVO_MAX = 300  # Max pulse length out of 4096


def stop_at_exit(engine):
    engine.stop_all_wheels()

def main():
    global pwm
    tof = VL53L0X.VL53L0X()
    print(tof.get_distance())
    print(os.path.dirname(os.path.abspath(__file__)))
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    print(os.path.dirname(os.path.abspath(__file__)))

    engine = Engine.Engine()
    atexit.register(stop_at_exit, engine)
    engine.move_all_wheels_forward(20)
    sleep(2)
    engine.move_all_wheels_backward(20)
    sleep(2)
    engine.stop_all_wheels()


    stop1 = 0
    stop2 = 0

    timing = tof.get_timing()
    if (timing < 20000):
        timing = 20000
    print("Timing %d ms" % (timing / 1000))

    while (1):
        pwm.set_pwm(0, 0, SERVO_MIN)
        time.sleep(0.5)
        distance = tof.get_distance()
        print("1: %d mm, %d cm" % (distance, (distance / 10)))
        if (distance > 200):
            engine.stop_all_wheels()
            stop1 = 1
            print("Stopp_1!")
        else:
            # c.move(30)
            stop1 = 0
            print("Frei_1!")
        # time.sleep(0.5)
        pwm.set_pwm(0, 0, SERVO_MAX)
        time.sleep(0.5)
        distance = tof.get_distance()
        print("2: %d mm, %d cm" % (distance, (distance / 10)))
        if (distance < 200):
            engine.stop_all_wheels()
            stop2 = 1
            print("Stopp_2!")
        else:
            # c.move(30)
            stop2 = 0
            print("Frei_2!")
        if (stop1 == 0 and stop2 == 0):
            engine.move_all_wheels_forward(20)


if __name__ == '__main__':
    main()
