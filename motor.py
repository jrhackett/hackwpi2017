import RPi.GPIO as GPIO
from time import sleep

class Motor:
	def __init__(self, motorPin1, motorPin2, motorEnable, dutyCycle):
		GPIO.setmode(GPIO.BCM)
		self.motorPin1 = motorPin1
		self.motorPin2 = motorPin2
		self.motorEnable = motorEnable
		self.dutyCycle = dutyCycle

		GPIO.setup(self.motorPin1, GPIO.OUT)
		GPIO.setup(self.motorPin2, GPIO.OUT)
		GPIO.setup(self.motorEnable, GPIO.OUT)
		setPWM = GPIO.PWM(self.motorEnable, self.dutyCycle)

	def clockwise(self):
		GPIO.output(self.motorPin1, GPIO.LOW)
		GPIO.output(self.motorPin2, GPIO.HIGH)
		GPIO.output(self.motorEnable, GPIO.HIGH)

	def counterclockwise(self):
		GPIO.output(self.motorPin1, GPIO.HIGH)
		GPIO.output(self.motorPin2, GPIO.LOW)
		GPIO.output(self.motorEnable, GPIO.HIGH)

	def stop(self):
		GPIO.output(self.motorPin1, GPIO.LOW)
		GPIO.output(self.motorPin2, GPIO.LOW)
		GPIO.output(self.motorEnable, GPIO.LOW)
