import serial
import time, math
import sys, tty, termios
import Adafruit_PCA9685
import VL53L0X
import Adafruit_GPIO.GPIO as GPIO
#Initialization at address 0x40
pwm = Adafruit_PCA9685.PCA9685()

servoMin = 200  # Min pulse length out of 4096
servoMax = 300  # Max pulse length out of 4096


class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class control:
    speed_right_wheels = 0
    speedM2 = 0

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
        self.ser.write([128, 0, x, (128 + x) & 0x7F])

    def move_right_wheels_backward(self, x):
        self.ser.write([128, 1, x, (129 + x) & 0x7F])

    def stop_right_wheels(self):
        self.ser.write([128, 0, 0, 128 & 0x7F])

    def move_left_wheels_backward(self, x):
        self.ser.write([128, 4, x, (132 + x) & 0x7F])

    def move_left_wheels_forward(self, x):
        self.ser.write([128, 5, x, (133 + x) & 0x7F])

    def stop_wheels_left(self):
        self.ser.write([128, 4, 0, 132 & 0x7F])

    def move_all_wheels_forward(self, x):
        self.move_right_wheels_forward(x)
        self.move_left_wheels_forward(x)

    def stop_all_wheels(self):
        self.stop_right_wheels()
        self.stop_wheels_left()

    def move_all_wheels_backward(self, x):
        self.move_right_wheels_backward(x)
        self.move_left_wheels_backward(x)

    def test(self):
        self.move_all_wheels_forward(40)
        time.sleep(3)
        self.stop_all_wheels()
        time.sleep(1)
        self.move_all_wheels_backward(40)
        time.sleep(3)
        self.stop_all_wheels()

    def up(self):
        if self.speed_right_wheels != self.speedM2:
            self.speed_right_wheels = ((self.speed_right_wheels + self.speedM2) / 2) - (((self.speed_right_wheels + self.speedM2) / 2) % 10)
            self.speedM2 = self.speed_right_wheels
        if self.speed_right_wheels >= 0 or self.speedM2 >= 0:
            self.speed_right_wheels += 10
            self.speedM2 += 10
            if self.speed_right_wheels > 120:
                self.speed_right_wheels = 120
            if self.speedM2 > 120:
                self.speedM2 = 120
            self.move_right_wheels_forward(self.speed_right_wheels)
            self.move_left_wheels_forward(self.speedM2)

        elif self.speed_right_wheels < 0 or self.speedM2 < 0:
            self.speed_right_wheels += 10
            self.speedM2 += 10
            if self.speed_right_wheels > 120:
                self.speed_right_wheels = 120
            if self.speedM2 > 120:
                self.speedM2 = 120
            self.move_right_wheels_backward(abs(self.speed_right_wheels))
            self.move_left_wheels_backward(abs(self.speedM2))

    #		if self.speedM1 == 0:
    #			self.stop()

    def down(self):
        if self.speed_right_wheels != self.speedM2:
            self.speed_right_wheels = ((self.speed_right_wheels + self.speedM2) / 2) - (((self.speed_right_wheels + self.speedM2) / 2) % 10)
            self.speedM2 = self.speed_right_wheels
        if self.speed_right_wheels > 0 or self.speedM2 > 0:
            self.speed_right_wheels -= 10
            self.speedM2 -= 10
            if self.speed_right_wheels > 120:
                self.speed_right_wheels = 120
            if self.speedM2 > 120:
                self.speedM2 = 120
            self.move_right_wheels_forward(self.speed_right_wheels)
            self.move_left_wheels_forward(self.speedM2)

        elif self.speed_right_wheels <= 0 or self.speedM2 <= 0:
            self.speed_right_wheels -= 10
            self.speedM2 -= 10
            if self.speed_right_wheels < -120:
                self.speed_right_wheels = -120
            if self.speedM2 < -120:
                self.speedM2 = -120
            self.move_right_wheels_backward(abs(self.speed_right_wheels))
            self.move_left_wheels_backward(abs(self.speedM2))

    #		if self.speedM1 == 0:
    #			self.stop()

    def left(self):
        if self.speed_right_wheels > 0 or self.speedM2 > 0:
            self.speed_right_wheels += 10
            self.speedM2 -= 10
            if self.speed_right_wheels > 120:
                self.speed_right_wheels = 120
            if self.speedM2 <= 0:
                self.speedM2 = 0
            self.move_right_wheels_forward(self.speed_right_wheels)
            self.move_left_wheels_forward(self.speedM2)

        elif self.speed_right_wheels < 0 or self.speedM2 < 0:
            self.speed_right_wheels += 10
            self.speedM2 -= 10
            if self.speed_right_wheels > 0:
                self.speed_right_wheels = 0
            if self.speedM2 > -120:
                self.speedM2 = -120
            self.move_right_wheels_backward(abs(self.speed_right_wheels))
            self.move_left_wheels_backward(abs(self.speedM2))

    def right(self):
        if self.speed_right_wheels > 0 or self.speedM2 > 0:
            self.speedM2 += 10
            self.speed_right_wheels -= 10
            if self.speedM2 > 120:
                self.speedM2 = 120
            if self.speed_right_wheels <= 0:
                self.speed_right_wheels = 0
            self.move_right_wheels_forward(self.speed_right_wheels)
            self.move_left_wheels_forward(self.speedM2)

        elif self.speed_right_wheels < 0 or self.speedM2 < 0:
            self.speedM2 += 10
            self.speed_right_wheels -= 10
            if self.speedM2 > 0:
                self.speedM2 = 0
            if self.speed_right_wheels < -120:
                self.speed_right_wheels = -120
            self.move_right_wheels_backward(abs(self.speed_right_wheels))
            self.move_left_wheels_backward(abs(self.speedM2))


def main():
    tof = VL53L0X.VL53L0X()
    tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    c = control()
    # c.test()
    # print 'Enter commands:'
    c.up()
    c.up()
    # c.up()

    stop1 = 0
    stop2 = 0

    timing = tof.get_timing()
    if (timing < 20000):
        timing = 20000
    print("Timing %d ms" % (timing / 1000))

    while (1):
        pwm.setPWM(0, 0, servoMin)
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
        pwm.setPWM(0, 0, servoMax)
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
