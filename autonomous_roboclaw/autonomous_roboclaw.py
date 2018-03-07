from time import sleep

import serial
import time
import Adafruit_PCA9685
import os
import VL53L0X as VL53L0X
import atexit

# Initialization at address 0x40
pwm = Adafruit_PCA9685.PCA9685()

SERVO_MIN = 200  # Min pulse length out of 4096
SERVO_MAX = 300  # Max pulse length out of 4096


def stop_at_exit(c):
    c.stop_all_wheels()


class control:
    global pwm
    speed_right_wheels = 0
    speed_left_wheels = 0

    def __init__(self):
        pass

    ser = serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    def move_right_wheels_forward(self, x):
        self.ser.write(bytes([128, 0, x, (128 + x) & 0x7F]))

    def move_right_wheels_backward(self, x):
        self.ser.write(bytes([128, 1, x, (129 + x) & 0x7F]))

    def stop_right_wheels(self):
        self.ser.write(bytes([128, 0, 0, 128 & 0x7F]))

    def move_left_wheels_backward(self, x):
        self.ser.write(bytes([128, 4, x, (132 + x) & 0x7F]))

    def move_left_wheels_forward(self, x):
        self.ser.write(bytes([128, 5, x, (133 + x) & 0x7F]))

    def stop_wheels_left(self):
        self.ser.write(bytes([128, 4, 0, 132 & 0x7F]))

    def move_all_wheels_forward(self, x):
        self.move_right_wheels_forward(x)
        self.move_left_wheels_forward(x)

    def stop_all_wheels(self):
        self.stop_right_wheels()
        self.stop_wheels_left()

    def move_all_wheels_backward(self, x):
        self.move_right_wheels_backward(x)
        self.move_left_wheels_backward(x)


def main():
    global pwm
    tof = VL53L0X.VL53L0X()
    print(tof.get_distance())
    print(os.path.dirname(os.path.abspath(__file__)))
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
    print(os.path.dirname(os.path.abspath(__file__)))

    c = control()
    atexit.register(stop_at_exit, c)
    c.move_all_wheels_forward(20)
    sleep(2)
    c.move_all_wheels_backward(20)
    sleep(2)
    c.stop_all_wheels()


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
            c.stop_all_wheels()
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
            c.stop_all_wheels()
            stop2 = 1
            print("Stopp_2!")
        else:
            # c.move(30)
            stop2 = 0
            print("Frei_2!")
        if (stop1 == 0 and stop2 == 0):
            c.move_all_wheels_forward(20)


if __name__ == '__main__':
    main()
