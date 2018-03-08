import serial, time


class Engine:
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

    def move_right_wheels_forward(self, speed):
        self.ser.write(bytes([128, 0, speed, (128 + speed) & 0x7F]))

    def move_right_wheels_backward(self, speed):
        self.ser.write(bytes([128, 1, speed, (129 + speed) & 0x7F]))

    def stop_right_wheels(self):
        self.ser.write(bytes([128, 0, 0, 128 & 0x7F]))

    def move_left_wheels_backward(self, speed):
        self.ser.write(bytes([128, 4, speed, (132 + speed) & 0x7F]))

    def move_left_wheels_forward(self, speed):
        self.ser.write(bytes([128, 5, speed, (133 + speed) & 0x7F]))

    def stop_left_wheels(self):
        self.ser.write(bytes([128, 4, 0, 132 & 0x7F]))

    def move_all_wheels_forward(self, speed):
        self.move_right_wheels_forward(speed)
        self.move_left_wheels_forward(speed)

    def stop_all_wheels(self):
        self.stop_right_wheels()
        self.stop_left_wheels()

    def move_all_wheels_backward(self, speed):
        self.move_right_wheels_backward(speed)
        self.move_left_wheels_backward(speed)

    def turn_around(self, speed = 35):
        self.move_right_wheels_forward(speed)
        self.move_left_wheels_backward(speed)
        time.sleep(2)


