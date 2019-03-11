import VL53L0X as VL53L0X
import RPi.GPIO as GPIO
import time
from enum import Enum


class State(Enum):
    FREE = 0
    BLOCKED = 1
    ERROR = 2


class TOFSensors:
    tof_f_right = None
    tof_f_left = None
    tof_b_right = None
    tof_b_left = None
    tof_h1 = None
    tof_h2 = None
    tof_h3 = None
    tof_h4 = None
    tof_h5 = None
    
    sensor_f_right_shutdown = 0
    sensor_f_left_shutdown = 0
    sensor_b_right_shutdown = 0
    sensor_b_left_shutdown = 0
    sensor_h1_shutdown = 0
    sensor_h2_shutdown = 0
    sensor_h3_shutdown = 0
    sensor_h4_shutdown = 0
    sensor_h5_shutdown = 0
    
    state_f_left_sensor = State.FREE
    state_f_right_sensor = State.FREE
    state_b_left_sensor = State.FREE
    state_b_right_sensor = State.FREE
    
    state_h1_sensor = State.FREE
    state_h2_sensor = State.FREE
    state_h3_sensor = State.FREE
    state_h4_sensor = State.FREE
    state_h5_sensor = State.FREE

    def __init__(self):
        # GPIO for Sensor f_right shutdown pin
        self.sensor_f_right_shutdown = 16
        # GPIO for Sensor f_left shutdown pin
        self.sensor_f_left_shutdown = 20
        # GPIO for Sensor Bf_left shutdown pin
        #self.sensor_b_right_shutdown = 17
        # GPIO for Sensor Bf_right shutdown pin 
        #self.sensor_b_left_shutdown = 27
        # GPIO for Sensors Head 1-5 from left to right shutdown pins
        self.sensor_h1_shutdown = 5
        self.sensor_h2_shutdown = 6
        self.sensor_h3_shutdown = 13
        self.sensor_h4_shutdown = 19
        self.sensor_h5_shutdown = 26
        
        GPIO.setwarnings(False)

        # Setup GPIO for shutdown pins on each VL53L0X
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.sensor_f_right_shutdown, GPIO.OUT)
        GPIO.setup(self.sensor_f_left_shutdown, GPIO.OUT)
        #GPIO.setup(self.sensor_b_right_shutdown, GPIO.OUT)
        #GPIO.setup(self.sensor_b_left_shutdown, GPIO.OUT)
        
        GPIO.setup(self.sensor_h1_shutdown, GPIO.OUT)
        GPIO.setup(self.sensor_h2_shutdown, GPIO.OUT)
        GPIO.setup(self.sensor_h3_shutdown, GPIO.OUT)
        GPIO.setup(self.sensor_h4_shutdown, GPIO.OUT)
        GPIO.setup(self.sensor_h5_shutdown, GPIO.OUT)
        

        # Set all shutdown pins low to turn off each VL53L0X
        GPIO.output(self.sensor_f_right_shutdown, GPIO.LOW)
        GPIO.output(self.sensor_f_left_shutdown, GPIO.LOW)
        #GPIO.output(self.sensor_b_right_shutdown, GPIO.LOW)
        #GPIO.output(self.sensor_b_left_shutdown, GPIO.LOW)
        
        GPIO.output(self.sensor_h1_shutdown, GPIO.LOW)
        GPIO.output(self.sensor_h2_shutdown, GPIO.LOW)
        GPIO.output(self.sensor_h3_shutdown, GPIO.LOW)
        GPIO.output(self.sensor_h4_shutdown, GPIO.LOW)
        GPIO.output(self.sensor_h5_shutdown, GPIO.LOW)

        # Keep all low for 500 ms or so to make sure they reset
        time.sleep(0.5)

        # Create one object per VL53L0X passing the address to give to
        # each.
        self.tof_f_right = VL53L0X.VL53L0X(address=0x2B)
        self.tof_f_left = VL53L0X.VL53L0X(address=0x2D)
        #self.tof_b_right = VL53L0X.VL53L0X(address=0x2F) 
        #self.tof_b_left = VL53L0X.VL53L0X(address=0x31) 
        
        self.tof_h1 = VL53L0X.VL53L0X(address=0x33)
        self.tof_h2 = VL53L0X.VL53L0X(address=0x35)
        self.tof_h3 = VL53L0X.VL53L0X(address=0x37)
        self.tof_h4 = VL53L0X.VL53L0X(address=0x39)
        self.tof_h5 = VL53L0X.VL53L0X(address=0x3b)
        

        # Set shutdown pin high for the first VL53L0X then
        # call to start ranging
        GPIO.output(self.sensor_f_right_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_f_right.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

        # Set shutdown pin high for the second VL53L0X then
        # call to start ranging
        GPIO.output(self.sensor_f_left_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_f_left.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        #GPIO.output(self.sensor_b_right_shutdown, GPIO.HIGH)
        #time.sleep(0.50)
        #self.tof_b_right.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        #GPIO.output(self.sensor_b_left_shutdown, GPIO.HIGH)
        #time.sleep(0.50)
        #self.tof_b_left.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        
        GPIO.output(self.sensor_h1_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_h1.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        GPIO.output(self.sensor_h2_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_h2.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        GPIO.output(self.sensor_h3_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_h3.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        GPIO.output(self.sensor_h4_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_h4.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
        
        GPIO.output(self.sensor_h5_shutdown, GPIO.HIGH)
        time.sleep(0.50)
        self.tof_h5.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

    def run(self):
        """
        Starts measuring the distance of the f_left and f_right sensor.
        Sets the state of the two sensors according to the distance measured.
        A sensor is blocked if the distance is less than 18 cm and more than 30 cm.
        A sensor is free if the distance is in between 18 and 30 cm.
        :return:
        """

        distance_f_right_sensor = self.tof_f_right.get_distance()
        distance_f_left_sensor = self.tof_f_left.get_distance()
        
        #distance_b_right_sensor = self.tof_b_right.get_distance()
        #distance_b_left_sensor = self.tof_b_left.get_distance()
        
        distance_h1_sensor = self.tof_h1.get_distance()
        distance_h2_sensor = self.tof_h2.get_distance()
        distance_h3_sensor = self.tof_h3.get_distance()
        distance_h4_sensor = self.tof_h4.get_distance()
        distance_h5_sensor = self.tof_h5.get_distance()
        
        print("Distance f_left sensor: {} , Distance f_right sensor: {}".format(str(distance_f_left_sensor),
                                                                            str(distance_f_right_sensor)))
        
        #print("Distance b_left sensor: {} , Distance b_right sensor: {}".format(str(distance_b_left_sensor),
         #                                                                   str(distance_b_right_sensor)))
        
        print("h1: {} , h2: {} , h3: {} , h4: {} , h5: {}".format(str(distance_h1_sensor),
                str(distance_h2_sensor), str(distance_h3_sensor), str(distance_h4_sensor), str(distance_h5_sensor)))
        
        if distance_f_right_sensor > 300:
            self.state_f_right_sensor = State.BLOCKED

        else:
            self.state_f_right_sensor = State.FREE

        if distance_f_left_sensor > 300:
            self.state_f_left_sensor = State.BLOCKED

        else:
            self.state_f_left_sensor = State.FREE
            
        if distance_h1_sensor < 170:
            self.state_h1_sensor = State.BLOCKED

        else:
            self.state_h1_sensor = State.FREE
            
        if distance_h2_sensor < 170:
            self.state_h2_sensor = State.BLOCKED

        else:
            self.state_h2_sensor = State.FREE
            
        if distance_h3_sensor < 180:
            self.state_h3_sensor = State.BLOCKED

        else:
            self.state_h3_sensor = State.FREE
            
        if distance_h4_sensor < 170:
            self.state_h4_sensor = State.BLOCKED

        else:
            self.state_h4_sensor = State.FREE
            
        if distance_h5_sensor < 170:
            self.state_h5_sensor = State.BLOCKED

        else:
            self.state_h5_sensor = State.FREE
            
        
