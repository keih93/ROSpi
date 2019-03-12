import Adafruit_PCA9685

class Servos:
    pwm = None
    
    # pin numbers
    SERVO_LEFT = 0
    SERVO_RIGHT = 1
    SERVO_FACE = 14  # horizontal
    SERVO_HEAD = 15  # vertical
    
    # experimentally determined values for the servo pwm's
    LEFT_DOWN = 780
    LEFT_FORWARD = 480
    
    RIGHT_DOWN = 780
    RIGHT_FORWARD = 1090
    
    FACE_FORWARD = 1260
    FACE_LEFT = FACE_FORWARD - 500
    FACE_RIGHT = FACE_FORWARD + 500
    
    HEAD_UP = 455  # == FORWARD, the robo cannot look up much
    HEAD_DOWN = 1200  # TODO
    
    def __init__(self):
        """constructor"""
        # Initialization at address 0x40
        self.pwm = Adafruit_PCA9685.PCA9685()
    
    def __del__(self):
        """destructor"""
        self.set_servo(self.SERVO_LEFT, 0)
        self.set_servo(self.SERVO_RIGHT, 0)
        self.set_servo(self.SERVO_FACE, 0)
        self.set_servo(self.SERVO_HEAD, 0)
    
    def set_servo(self, servo, value):  # servos.set_serveo(SERVO.FRONT, Servo.FRONT_FORWARD)
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
        self.set_servo(self.SERVO_LEFT, self.LEFT_DOWN)
    
    def right_servo_down(self):
        """
        Moves right servo to face the ground.
        :return:
        """
        self.set_servo(self.SERVO_RIGHT, self.RIGHT_DOWN)
    
    def both_servos_down(self):
        """
        Moves left and right servo to face the ground.
        :return:
        """
        self.set_servo(self.SERVO_LEFT, self.LEFT_DOWN)
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
    
    def both_servos_forward(self):
        """
        Moves left and right servo to face forward.
        :return:
        """
        self.set_servo(self.SERVO_LEFT, self.LEFT_FORWARD)
        self.set_servo(self.SERVO_RIGHT, self.RIGHT_FORWARD)
    
    def front_servo_forward(self):
        """
        Moves front servo to face forward.
        :return:
        """
        self.set_servo(self.SERVO_FACE, self.FACE_FORWARD)
    