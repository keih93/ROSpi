from picamera.array import PiRGBArray
from picamera import PiCamera
from camera import CameraThread
from Engine import Engine
from Servos import Servo, Servos
import time


camera = PiCamera()
engine = Engine();
servos = Servos();
servoFace = servos.servoFace
servoHead = servos.servoHead
servoTail = servos.servoTail

def testCamera():
    print("Testing camera: After 3 seconds your screen should show the camera output.")
    print("If the output is black, make sure that you removed the lens cap!")
    time.sleep(2)
    camera.rotation = 180
    camera.start_preview()
    time.sleep(3)
    camera.stop_preview()
    camera.close()

def testEngine():
    print("Testing the engine")
    print("move left wheels..")
    engine.move_left_wheels_forward()
    time.sleep(1)
    engine.stop_left_wheels()
    print("move right wheels..")
    engine.move_right_wheels_forward()
    time.sleep(1)
    engine.stop_right_wheels()
    time.sleep(0.5)

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
    moveServoForward = True
    now = time.time()
    future = now + 2
    while time.time() < future:
        time.sleep(0.01)
        if moveServoForward:
            servo.addval(10)
            if servo.val >= servo.max_val:
                moveServoForward = False
        else:
            servo.addval(-10)
            if servo.val <= servo.min_val:
                moveServoForward = True
        pass
    
    servo.reset()
    time.sleep(0.5)

def main():
    print("The robots functionality is now tested for each module...")
    testCamera()
    testEngine()
    testTailServo()
    testHeadServo()
    testFaceServo()


if __name__ == "__main__":
    main()