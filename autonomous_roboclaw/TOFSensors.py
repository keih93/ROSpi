import VL53L0X as VL53L0X
import RPi.GPIO as GPIO
import time
from enum import Enum


class State(Enum):
    FREE = 0
    BLOCKED = 1
    ERROR = 2


class TOFSensors:
    tof_right = None
    tof_left = None
    sensor_right_shutdown = 0
    sensor_left_shutdown = 0
    state_left_sensor = State.FREE
    state_right_sensor = State.FREE

    def __init__(self):
        # GPIO for Sensor 1 shutdown pin
        self.sensor_right_shutdown = 20
        # GPIO for Sensor 2 shutdown pin
        self.sensor_left_shutdown = 16

        GPIO.setwarnings(False)

        # Setup GPIO for shutdown pins on each VL53L0X
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_right_shutdown, GPIO.OUT)
        GPIO.setup(self.sensor_left_shutdown, GPIO.OUT)

        # Set all shutdown pins low to turn off each VL53L0X
        GPIO.output(self.sensor_right_shutdown, GPIO.LOW)
        GPIO.output(self.sensor_left_shutdown, GPIO.LOW)

        # Keep all low for 500 ms or so to make sure they reset
        time.sleep(0.50)

        # Create one object per VL53L0X passing the address to give to
        # each.
        self.tof_right = VL53L0X.VL53L0X(address=0x2B)
        self.tof_left = VL53L0X.VL53L0X(address=0x2D)

        # Set shutdown pin high for the first VL53L0X then
        # call to start ranging
        GPIO.output(self.sensor_right_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_right.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        # Set shutdown pin high for the second VL53L0X then
        # call to start ranging
        GPIO.output(self.sensor_left_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_left.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        # GPIO for Sensor 1 shutdown pin
        self.sensor_right_shutdown = 20
        # GPIO for Sensor 2 shutdown pin
        self.sensor_left_shutdown = 16

    def run(self):
        """
        Starts measuring the distance of the left and right sensor.
        Sets the state of the two sensors according to the distance measured.
        A sensor is blocked if the distance is less than 18 cm and more than 30 cm.
        A sensor is free if the distance is in between 18 and 30 cm.
        :return:
        """

        distance_right_sensor = self.tof_right.get_distance()
        distance_left_sensor = self.tof_left.get_distance()
        print("Distance Left sensor: {} , Distance Right sensor: {}".format(str(distance_left_sensor),
                                                                            str(distance_right_sensor)))

        if distance_right_sensor < 180 or distance_right_sensor > 300:
            self.state_right_sensor = State.BLOCKED

        else:
            self.state_right_sensor = State.FREE

        if distance_left_sensor < 180 or distance_left_sensor > 300:
            self.state_left_sensor = State.BLOCKED

        else:
            self.state_left_sensor = State.FREE
