from picamera.array import PiRGBArray
from picamera import PiCamera
from camera import CameraThread
from Engine import Engine
from Servos import Servo, Servos
import time

camera = PiCamera()
engine = Engine();
servos = Servos();
servoFace = s.servoFace
servoHead = s.servoHead
servoTail = s.servoTail

moveServoForward = True

def testCamera():
    print("Testing camera: After 3 seconds your screen should show the camera output.")
    print("If the output is black, make sure that you removed the lens cap!")
    time.sleep(3)
    self.camera.start_preview()
    time.sleep(5)
    self.camera.stop_preview()
    camera.close()

def testEngine():
    print("Testing the engine")
    print("move left wheels..")
    self.engine.move_left_wheels_forward()
    time.sleep(2)
    self.engine.stop_left_wheels()
    print("move right wheels..")
    self.engine.move_right_wheels_forward()
    time.sleep(2)
    self.engine.stop_right_wheels()

def testTailServo():
    print("Testing tail servos")
    testServo(servoTail)

def testHeadServo():
    print("Testing head servo")
    testServo(servoHead)

def testFaceServo():
    print("Testing face servo")
    testServo(servoFace)

def testServo(servo):
    now = time.time()
    future = now + 3
    while time.time() < future:
        if self.moveServoForward:
            servo.addval(80)
            if servo.val >= servo.max_val:
                self.moveServoForward = False
        else:
            servo.addval(-80)
            if servo.val <= servo.min_val:
                self.moveServoForward = True
        pass

    servo.setVal(0)

def main():
    print("The robots functionality is now tested for each module...")
    testCamera()
    testEngine()
    testTailServo()
    testHeadServo()
    testFaceServo()


if __name__ == "__main__":
    main()