
import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)

#motorPin1 and motorPin2 controllers 
motorPin1 = 	
motorPin2 = 
motorEnable = 
dutyCycle = 

def motInit():
	GPIO.setup(motorPin1, GPIO.OUT)
	GPIO.setup(motorPin2, GPIO.OUT)
	GPIO.setup(motorEnable, GPIO.OUT)
	setPWM = GPIO.PWM(motorEnable, dutyCycle)	

#Rotate Motor in the clockwise direction
def motorC():
	GPIO.output(motorPin1, GPIO.HIGH)
	GPIO.output(motorPin2, GPIO.LOW)
	GPIO.output(motorEnable, GPIO.HIGH)

#Rotate Motor in the anticlockwise Direction
def motorAC():
	GPIO.output(motorPin1, GPIO.LOW)
	GPIO.output(motorPin2, GPIO.HIGH)
	GPIO.output(motorEnable, GPIO.HIGH)

#Stop Motor

def motorDo(direction):
	#case 0: roll down
	#case 1: roll up
	#case 2: stop 
	switch(direction){
		case 0:
			motC()
			break;
		case 1: 
			motAC()
			break;
		case 2:
			GPIO.output(motorEnable, GPIO.LOW)
			break;
	}

def motorTime():
	sleep(2) #Keeps motor on for sleep 2 seconds

def motStatus():
	#check the status of the entire system and then choose the motor direction


