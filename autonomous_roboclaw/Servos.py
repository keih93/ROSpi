import Adafruit_PCA9685

class Servos:
    pwm = None
    
    LEFT_SERVO = 0
    RIGHT_SERVO = 1
    FRONT_SERVO = 3
    
    LEFT_DOWN = 780
    LEFT_FORWARD = 480
    RIGHT_DOWN = 780
    RIGHT_FORWARD = 1090
    FRONT_FORWARD = 1350
    
    def __init__(self):
        # Initialization at address 0x40
        self.pwm = Adafruit_PCA9685.PCA9685()
    
    def set_servo(self, servo, value):
        """
        Triggers given servo to move to given position.
        :param servo: servo to move
        :param value: position to move to
        :return:
        """
        self.pwm.set_pwm(servo, 0, value)
    
    def left_servo_down(self):
        """
        Moves left servo to face the ground.
        :return:
        """
        self.set_servo(self.LEFT_SERVO, self.LEFT_DOWN)
    
    def right_servo_down(self):
        """
        Moves right servo to face the ground.
        :return:
        """
        self.set_servo(self.RIGHT_SERVO, self.RIGHT_DOWN)
    
    def both_servos_down(self):
        """
        Moves left and right servo to face the ground.
        :return:
        """
        self.set_servo(self.LEFT_SERVO, self.LEFT_DOWN)
        self.set_servo(self.RIGHT_SERVO, self.RIGHT_DOWN)
    
    def left_servo_forward(self):
        """
        Moves left servo to face forward.
        :return:
        """
        self.set_servo(self.LEFT_SERVO, self.LEFT_FORWARD)
    
    def right_servo_forward(self):
        """
        Moves right servo to face forward.
        :return:
        """
        self.set_servo(self.RIGHT_SERVO, self.RIGHT_FORWARD)
    
    def both_servos_forward(self):
        """
        Moves left and right servo to face forward.
        :return:
        """
        self.set_servo(self.LEFT_SERVO, self.LEFT_FORWARD)
        self.set_servo(self.RIGHT_SERVO, self.RIGHT_FORWARD)
    
    def front_servo_forward(self):
        """
        Moves front servo to face forward.
        :return:
        """
        self.set_servo(self.FRONT_SERVO, self.FRONT_FORWARD)
    