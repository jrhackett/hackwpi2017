import RPi.GPIO as GPIO
from time import sleep

class Toaster:
	def __init__(self, heaterEnablePin, solenoidPin, toasterPin, heaterSelectPin):
		self.heaterEnablePin = heaterEnablePin
		self.solenoidPin = solenoidPin
		self.toasterPin = toasterPin
		self.heaterSelectPin = heaterSelectPin
		self.bagelEnabled = False

		GPIO.setup(self.heaterEnablePin, GPIO.OUT)
		GPIO.setup(self.solenoidPin, GPIO.OUT)
		GPIO.setup(self.toasterPin, GPIO.IN)
		GPIO.setup(self.heaterSelectPin, GPIO.OUT)

	def enable_solenoid():
		GPIO.output(self.solenoidPin, GPIO.LOW)

	def disable_solenoid():
		GPIO.output(self.solenoidPin, GPIO.HIGH)

	def enable_heater():
		GPIO.output(self.heaterEnablePin, GPIO.LOW)

	def disable_heater():
		GPIO.output(self.heaterEnablePin, GPIO.HIGH)

	def is_toaster_on():
		return not GPIO.input(self.toasterPin)

	def is_bagel_mode():
		return self.bagelEnabled

	def enable_bagel_mode():
		self.bagelEnabled = True

	def disable_bagel_mode():
		self.bagelEnabled = False

	def enable_outside():
		GPIO.output(self.heaterSelectPin, GPIO.HIGH)

	def enable_inside():
		GPIO.output(self.heaterSelectPin, GPIO.LOW)
