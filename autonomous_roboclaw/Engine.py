import serial


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

    def stop_left_wheels(self):
        self.ser.write(bytes([128, 4, 0, 132 & 0x7F]))

    def move_all_wheels_forward(self, x):
        self.move_right_wheels_forward(x)
        self.move_left_wheels_forward(x)

    def stop_all_wheels(self):
        self.stop_right_wheels()
        self.stop_left_wheels()

    def move_all_wheels_backward(self, x):
        self.move_right_wheels_backward(x)
        self.move_left_wheels_backward(x)
