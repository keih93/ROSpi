# -*- coding: utf-8 -*-
import math

import Adafruit_PCA9685


# global static
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


class Servo(object):
    """
    Struct class holding information about each servo and some helper methods.
    """
    def __init__(self, pin, min_val, max_val, min_deg, max_deg, val=None, name=None):
        self.pin = pin
        self.min_val = min_val
        self.max_val = max_val
        self.min_deg = min_deg
        self.max_deg = max_deg
        self.name = name if name is not None else "Servo_" + str(self.pin)
        
        # the initially set value, default to middle
        self.setval(val if val is not None else (self.min_val + self.max_val) / 2)
        self.initial_val = self.val  # useful for reset
    
    def reset(self):
        self.setval(self.initial_val)
    
    def setval(self, val):
        """
        Set the current servo value, clamped between its min and max.
        """
        self.val = int(max(min(val, self.max_val), self.min_val))
        
        # apply val to hardware
        pwm.set_pwm(self.pin, 0, self.val)
        
        return self.val
    
    def addval(self, val):
        """
        Add the given value to the current servo value.
        """
        # round relative value away from zero
        if val > 0:
            val = int(round(val + 0.5))
        elif val < 0:
            val = int(round(val - 0.5))
        self.setval(self.val + val)  
    
    def val2degree(self):
        """
        Get the current servo value in degree.
        """
        val_rel = (float(self.val - self.min_val) / (self.max_val - self.min_val))
        deg_span = (self.max_deg - self.min_deg)
        deg_step = val_rel * deg_span
        return self.min_deg + deg_step
    
    def degree2val(self, angle_degree):
        """
        Get the servo value for an angle in degree.
        """
        deg_rel = (float(angle_degree - self.min_deg) / (self.max_deg - self.min_deg))
        val_span = (self.max_val - self.min_val)
        val_step = deg_rel * val_span
        return self.min_val + val_step
        
    def val2rad(self):
        """
        Get the current servo value in radians.
        """
        return math.pi * self.val2degree() / 180
        
    def rad2val(self, angle_rad):
        """
        Get the servo value for an angle in radians.
        """
        return self.degree2val((360/(2 * math.pi)) * angle_rad)

class Servos:
    pwm = None
    
    # servo pins
    SERVO_LEFT = 0
    SERVO_RIGHT = 1
    SERVO_FACE = 14  # horizontal
    SERVO_HEAD = 15  # vertical
    SERVO_TAIL = 8
    
    # experimentally determined values for the servo pwm's
    # Currently valid for: pwm.set_pwm_freq(50)
    LEFT_DOWN = 780  # TODO check if still correct
    LEFT_FORWARD = 480  # TODO check if still correct
    
    RIGHT_DOWN = 780  # TODO check if still correct
    RIGHT_FORWARD = 1090  # TODO check if still correct
    
    FACE_FORWARD = 325
    FACE_LEFT = FACE_FORWARD - 150
    FACE_RIGHT = FACE_FORWARD + 150
    
    HEAD_UP = 175
    HEAD_FORWARD = 225
    HEAD_DOWN = 300
    
    # servo objects
    servoLeftTOF = Servo(pin=SERVO_LEFT,
                         min_val=LEFT_DOWN,
                         max_val=350,  # TODO test max_val 
                         min_deg=-45,  # TODO measure
                         max_deg=0,    # TODO measure
                         val=LEFT_FORWARD,
                         name="Servo_left")
    
    servoRightTOF = Servo(pin=SERVO_RIGHT,
                          min_val=RIGHT_DOWN,
                          max_val=1200,  # TODO test max_val 
                          min_deg=-45,   # TODO measure
                          max_deg=0,     # TODO measure
                          val=RIGHT_FORWARD,
                          name="Servo_right")
    
    servoFace = Servo(pin=14,
                      min_val=FACE_LEFT,
                      max_val=FACE_RIGHT,
                      min_deg=-80,
                      max_deg=80,
                      val=FACE_FORWARD,
                      name="Servo_face")
    
    servoHead = Servo(pin=15,
                      min_val=HEAD_UP,
                      max_val=HEAD_DOWN,
                      min_deg=-25,
                      max_deg=90,
                      val=HEAD_FORWARD,
                      name="Servo_head")
    
    servoTail = Servo(pin=8,
                      min_val=280,
                      max_val=400,
                      min_deg=0,
                      max_deg=90,
                      val=350,
                      name="Servo_tail")
    
    
    
    def __init__(self):
        """constructor"""
        self.pwm = pwm  # XXX get global var as class var to save refactoring
        
        # list of "official" servos this module manages:
        self.all_servos = [Servos.servoLeftTOF, Servos.servoRightTOF, Servos.servoFace, Servos.servoHead, Servos.servoTail]
    
    def __del__(self):
        """destructor: reset all servos"""
        for s in self.all_servos:
            self.set_servo(s.pin, 0)
    
    def set_servo(self, servo, value):
        """
        Triggers given servo to move to given position.
        
        Example:
            >>> servos.set_serveo(Servos.SERVO_FRONT, Servo.FRONT_FORWARD)
        
        :param servo: servo to move
        :param value: position to move to
        :return:
        """
        if isinstance(servo, int):
            # set by pin number, NO checks!
            self.pwm.set_pwm(servo, 0, value)
        elif isinstance(servo, Servo):
            # set on servo object, safe
            servo.setval(value)
            print(u"%s is now set to %s°" % (servo.name, servo.val2degree()))
    
    def reset(self):
        """Reset all servos to default"""
        for s in self.all_servos:
            s.reset()
    
    def left_servo_down(self):
        """
        Moves left servo to face the ground.
        :return:
        """
        self.set_servo(self.SERVO_LEFT, self.LEFT_DOWN)
    
    def right_servo_down(self):
        """
        Moves right servo to face the ground.
        :return:
        """
        self.set_servo(self.SERVO_RIGHT, self.RIGHT_DOWN)
    
    def left_servo_forward(self):
        """
        Moves left servo to face forward.
        :return:
        """
        self.set_servo(self.SERVO_LEFT, self.LEFT_FORWARD)
    
    def right_servo_forward(self):
        """
        Moves right servo to face forward.
        :return:
        """
        self.set_servo(self.SERVO_RIGHT, self.RIGHT_FORWARD)
    
    def side_servos_forward(self):
        """
        Moves left and right servo to face forward.
        :return:
        """
        self.set_servo(self.SERVO_LEFT, self.LEFT_FORWARD)
        self.set_servo(self.SERVO_RIGHT, self.RIGHT_FORWARD)
    