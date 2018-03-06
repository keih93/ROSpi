import serial
import time, math
import sys,tty,termios
from Adafruit_PWM_Servo_Driver import PWM
import VL53L0X
import RPi.GPIO as GPIO

pwm = PWM(0x40)

servoMin = 200  # Min pulse length out of 4096
servoMax = 300  # Max pulse length out of 4096


class _Getch:
    def __call__(self):
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(3)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

class controll:
	speedM1=0
	speedM2=0

	def __init__(self):
		pass

	ser = serial.Serial(
		port = '/dev/ttyUSB0',
		baudrate = 19200,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS
	)

	def moveM1(self, x):
		self.ser.write([128,0,x,(128+x) & 0x7F])

	def moveBM1(self, x):
		self.ser.write([128,1,x,(129+x) & 0x7F])

	def stopM1(self):
		self.ser.write([128,0,0,128 & 0x7F])
	
	def moveBM2(self, x):
		self.ser.write([128,4,x,(132+x) & 0x7F])
	
	def moveM2(self, x):
		self.ser.write([128,5,x,(133+x) & 0x7F])
	
	def stopM2(self):
		self.ser.write([128,4,0,132 & 0x7F])
	
	def move(self, x):
		self.moveM1(x)
		self.moveM2(x)
	
	def stop(self):
		self.stopM1()
		self.stopM2()
	
	def moveB(self, x):
		self.moveBM1(x)
		self.moveBM2(x)
	
	def test(self):
		self.move(40)
		time.sleep(3)
		self.stop()
		time.sleep(1)
		self.moveB(40)
		time.sleep(3)
		self.stop()

	def up(self):
		if self.speedM1 != self.speedM2:
			self.speedM1 = ((self.speedM1+self.speedM2)/2)-(((self.speedM1+self.speedM2)/2) % 10)
			self.speedM2 = self.speedM1
		if self.speedM1 >= 0 or self.speedM2 >= 0:
			self.speedM1 += 10
			self.speedM2 += 10
			if self.speedM1 > 120:
				self.speedM1 = 120
			if self.speedM2 > 120:
				self.speedM2 = 120
			self.moveM1(self.speedM1)
			self.moveM2(self.speedM2)

		elif self.speedM1 < 0 or self.speedM2 < 0:
			self.speedM1 += 10
			self.speedM2 += 10
			if self.speedM1 > 120:
				self.speedM1 = 120
			if self.speedM2 > 120:
				self.speedM2 = 120
			self.moveBM1(abs(self.speedM1))
			self.moveBM2(abs(self.speedM2))
#		if self.speedM1 == 0:
#			self.stop()

	def down(self):
		if self.speedM1 != self.speedM2:
			self.speedM1 = ((self.speedM1+self.speedM2)/2)-(((self.speedM1+self.speedM2)/2) % 10)
			self.speedM2 = self.speedM1
		if self.speedM1 > 0 or self.speedM2 > 0:
			self.speedM1 -= 10
			self.speedM2 -= 10
			if self.speedM1 > 120:
				self.speedM1 = 120
			if self.speedM2 > 120:
				self.speedM2 = 120
			self.moveM1(self.speedM1)
			self.moveM2(self.speedM2)

		elif self.speedM1 <= 0  or self.speedM2 <= 0:
			self.speedM1 -= 10
			self.speedM2 -= 10
			if self.speedM1 < -120:
				self.speedM1 = -120
			if self.speedM2 < -120:
				self.speedM2 = -120
			self.moveBM1(abs(self.speedM1))
			self.moveBM2(abs(self.speedM2))
#		if self.speedM1 == 0:
#			self.stop()

	def left(self):
		if self.speedM1 > 0  or self.speedM2 > 0:
			self.speedM1 += 10
			self.speedM2 -= 10
			if self.speedM1 > 120:
				self.speedM1 = 120
			if self.speedM2 <= 0:
				self.speedM2 = 0
			self.moveM1(self.speedM1)
			self.moveM2(self.speedM2)

		elif self.speedM1 < 0  or self.speedM2 < 0:
			self.speedM1 += 10
			self.speedM2 -= 10
			if self.speedM1 > 0:
				self.speedM1 = 0
			if self.speedM2 > -120:
				self.speedM2 = -120
			self.moveBM1(abs(self.speedM1))
			self.moveBM2(abs(self.speedM2))


	def right(self):
		if self.speedM1 > 0  or self.speedM2 > 0:
			self.speedM2 += 10
			self.speedM1 -= 10
			if self.speedM2 > 120:
				self.speedM2 = 120
			if self.speedM1 <= 0:
				self.speedM1 = 0
			self.moveM1(self.speedM1)
			self.moveM2(self.speedM2)

		elif self.speedM1 < 0 or self.speedM2 < 0:
			self.speedM2 += 10
			self.speedM1 -= 10
			if self.speedM2 > 0:
				self.speedM2 = 0
			if self.speedM1 < -120:
				self.speedM1 = -120
			self.moveBM1(abs(self.speedM1))
			self.moveBM2(abs(self.speedM2))


def main():
	tof = VL53L0X.VL53L0X()
	tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)

	c = controll()
	#c.test()
	#print 'Enter commands:'
	c.up()
	c.up()
	#c.up()

	stop1 = 0
	stop2 = 0

	timing = tof.get_timing()
	if (timing < 20000):
		timing = 20000
	print ("Timing %d ms" % (timing/1000))

	while(1):
		pwm.setPWM(0, 0, servoMin)
		time.sleep(0.5)
		distance = tof.get_distance()
		print ("1: %d mm, %d cm" % (distance, (distance/10)))
		if (distance > 200):
			c.stop()
			stop1 = 1
			print("Stopp_1!")
		else: 
			#c.move(30)
			stop1 = 0
			print("Frei_1!")
		#time.sleep(0.5)
		pwm.setPWM(0, 0, servoMax)
		time.sleep(0.5)
		distance = tof.get_distance()
		print ("2: %d mm, %d cm" % (distance, (distance/10)))
		if (distance < 200):
			c.stop()
			stop2 = 1
			print("Stopp_2!")
		else: 
			#c.move(30)
			stop2 = 0
			print("Frei_2!")
		if (stop1 == 0 and stop2 == 0):
			c.move(20)
		#time.sleep(0.5)


		#inkey = _Getch()
		#while(1)
		#	k=inkey()
		#	if k!='':break
		#if k=='\x1b[A':
			#print "up"
		#	c.up()
			#print c.speedM1
			#print c.speedM2
		#elif k=='\x1b[B':
			#print "down"
		#	c.down()
			#print c.speedM1
			#print c.speedM2
		#elif k=='\x1b[C':
			#print "right"
		#	c.right()
			#print c.speedM1
			#print c.speedM2
		#elif k=='\x1b[D':
			#print "left"
		#	c.left()
			#print c.speedM1
			#print c.speedM2
		#else:
			#print "not an arrow key!"
		#	c.stop()
		#	break

if __name__=='__main__':
	main()


