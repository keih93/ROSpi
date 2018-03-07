import VL53L0X as VL53L0X
import RPi.GPIO as GPIO
import time


class TOFSensor:
    tof_left = None
    tof_right= None
    sensor_left_shutdown = 0
    sensor_right_shutdown = 0

    def __init__(self):
        # GPIO for Sensor 1 shutdown pin
        self.sensor_left_shutdown = 20
        # GPIO for Sensor 2 shutdown pin
        self.sensor_right_shutdown = 16

        GPIO.setwarnings(False)

        # Setup GPIO for shutdown pins on each VL53L0X
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_left_shutdown, GPIO.OUT)
        GPIO.setup(self.sensor_right_shutdown, GPIO.OUT)

        # Set all shutdown pins low to turn off each VL53L0X
        GPIO.output(self.sensor_left_shutdown, GPIO.LOW)
        GPIO.output(self.sensor_right_shutdown, GPIO.LOW)

        # Keep all low for 500 ms or so to make sure they reset
        time.sleep(0.50)

        # Create one object per VL53L0X passing the address to give to
        # each.
        self.tof_left = VL53L0X.VL53L0X(address=0x2B)
        self.tof_right = VL53L0X.VL53L0X(address=0x2D)

        # Set shutdown pin high for the first VL53L0X then
        # call to start ranging
        GPIO.output(self.sensor_left_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_left.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        # Set shutdown pin high for the second VL53L0X then
        # call to start ranging
        GPIO.output(self.sensor_right_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_right.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        # GPIO for Sensor 1 shutdown pin
        self.sensor_left_shutdown = 20
        # GPIO for Sensor 2 shutdown pin
        self.sensor_right_shutdown = 16
