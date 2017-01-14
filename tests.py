from motor import Motor
from toaster import Toaster
import RPi.GPIO as GPIO
import logging
import datetime
import time
from time import sleep

motor = Motor(0, 1, 2, 3) # TODO change these values to the actual pins and duty cycle
toaster = Toaster(0, 1, 2, 3) # TODO change these values to the actual pins

def engage_toaster():
    motor.clockwise()
    while(not toaster.is_toaster_on()):
        pass
    toaster.enable_solenoid()
    motor.stop()
    toaster.enable_heater()

def test_engage_toaster():
	engage_toaster()

def release_toaster():
    toaster.disable_heater()
    motor.counterclockwise()
    sleep(2)
    motor.stop()
    toaster.disable_solenoid()

def test_release_toaster():
	release_toaster()

def test_cycle_heat():
	wait_time = 120
	start_time = time.time()
	diff = time.time() - start_time
	outside = False
	while(diff > wait_time):
		if(diff % 5 == 0):
			if(outside):
				toaster.enable_inside()
			else:
				toaster.enable_outside()
		diff = time.time() - start_time

def make_localtime(tstr):
    """Convert HH:MM in UTC to HH:MM in local timezone."""
    # hours west of UTC
    offset_h = time.timezone // 3600 # hours west of UTC
    # subtract offset, reduce mod24, cast to str
    local_h = str((int(tstr[:2]) - offset_h + 24) % 24)
    # get minutes
    local_m = tstr[3:]
    return "{}:{}".format(local_h, local_m)

def test_time_conversion():
	t_old = "17:30"
	t_new = make_localtime(t_old)

	print("UTC time\t{}".format(t_old))
	print("Local time\t{}".format(t_new))

if __name__ == "__main__":
    pass