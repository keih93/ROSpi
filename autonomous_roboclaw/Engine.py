# -*- coding: utf-8 -*-
import serial
from roboclaw import Roboclaw


class Engine:
    def __init__(self):
        self.address = 0x80
        self.roboclaw = Roboclaw( "/dev/ttyS0", 38400 )
        self.roboclaw.Open()

    def __del__(self):
        """destructor"""
        self.stop_all_wheels()

    def move_right_wheels_forward(self, speed=50):
        """
        Move the right wheels forward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.roboclaw.ForwardM1( self.address, speed )

    def move_right_wheels_backward(self, speed=50):
        """
        Move the right wheels backward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.roboclaw.BackwardM1( self.address, speed )

    def stop_right_wheels(self):
        """
        Stop the right wheels by setting speed to 0
        :return:
        """
        self.roboclaw.ForwardM1( self.address, 0 )

    def move_left_wheels_backward(self, speed=50):
        """
        Move the left wheels backward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.roboclaw.BackwardM2( self.address, speed )

    def move_left_wheels_forward(self, speed=50):
        """
        Move the left wheels backward with a default speed of 50. Another speed can be provided by calling the
        function with a speed parameter.
        :param speed: An int which indicates the speed
        :return:
        """
        self.roboclaw.ForwardM2( self.address, speed )

    def stop_left_wheels(self):
        """
        Stop the left wheels by setting speed to 0
        :return:

        """
        self.roboclaw.ForwardM2( self.address, 0 )

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
