import serial


class Engine:
    speed_right_wheels = 0
    speed_left_wheels = 0

    def __init__(self):
        pass

    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=2400,  # 19200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )

    def move_right_wheels_forward(self, speed=50):
        """
        Move the right wheels forward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.ser.write(bytes([128, 0, speed, ((128 + speed) & 0x7F)]))

    def move_right_wheels_backward(self, speed=50):
        """
        Move the right wheels backward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.ser.write(bytes([128, 1, speed, ((129 + speed) & 0x7F)]))

    def stop_right_wheels(self):
        """
        Stop the right wheels by setting speed to 0
        :return:
        """
        self.ser.write(bytes([128, 0, 0, (128 & 0x7F)]))

    def move_left_wheels_backward(self, speed=50):
        """
        Move the left wheels backward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.ser.write(bytes([128, 4, speed, ((132 + speed) & 0x7F)]))

    def move_left_wheels_forward(self, speed=50):
        """
        Move the left wheels backward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.ser.write(bytes([128, 5, speed, ((133 + speed) & 0x7F)]))


    def stop_left_wheels(self):
        """
        Stop the left wheels by setting speed to 0
        :return:

        """
        self.ser.write(bytes([128, 4, 0, (132 & 0x7F)]))

    def move_all_wheels_forward(self, speed=50):
        """
        Move all wheels forward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:

        """
        self.move_right_wheels_forward(speed)
        self.move_left_wheels_forward(speed)

    def stop_all_wheels(self):
        """
        Stop all wheels by setting speed to 0
        :return:
        """
        self.stop_right_wheels()
        self.stop_left_wheels()

    def move_all_wheels_backward(self, speed=50):
        """
        Move all wheels backward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.move_right_wheels_backward(speed)
        self.move_left_wheels_backward(speed)

    def turn_around_left(self, speed=35):
        """
        Performs a left-hand turn on the spot by rotating the wheels in opposite directions.
        Right wheels forward and left wheels backward. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.move_right_wheels_forward(speed)
        self.move_left_wheels_backward(speed)


    def turn_around_right(self, speed=35):
        """
        Performs a right-hand turn on the spot by rotating the wheels in opposite directions.
        Left wheels forward and right wheels backward. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.move_right_wheels_backward(speed)
        self.move_left_wheels_forward(speed)
