import sys, getopt
from motor import Motor
from toaster import Toaster
import datetime
from datetime import time as time2
import time
from time import sleep

motor = Motor(13, 19, 6, 100)
toaster = Toaster(25, 8, 24, 7)

# wait_start from answer from http://stackoverflow.com/questions/6579127/delay-a-task-until-certain-time
def wait_start(runTime, action):
  times = runTime.split(':')
  times[0] = int(times[0])
  times[1] = int(times[1])
  startTime = time2(times[0], times[1])
  while startTime > datetime.datetime.time(datetime.datetime.now()): # you can add here any additional variable to break loop if necessary
      sleep(1)# you can change 1 sec interval to any other
  return action

def release_toaster():
  toaster.disable_heater()
  motor.counterclockwise()
  sleep(2.5)
  motor.stop()
  toaster.disable_solenoid()

def engage_toaster():
  motor.clockwise()
  print toaster.is_toaster_on()
  while(not toaster.is_toaster_on()):
      pass
  toaster.enable_solenoid()
  sleep(4.5)
  motor.stop()
  toaster.enable_heater()

def toast(wait_time):
  print "[1] Engaging the toaster"
  engage_toaster()
  print "[1] Toaster engaged"
  end_time = float(wait_time)
  start_time = time.time()
  diff = time.time() - start_time
  outside = True
  previous = 0

  toaster.enable_outside  ## TODO REMOVE THIS IF WE WANT DUTY CYCLES BACK

  while(diff < end_time):
    # tmp = int(diff)
    # if(outside):
    #   if(tmp != previous and (tmp - previous) % 10 == 0):
    #     previous = tmp
    #     print "[1] " + str(int(end_time - diff)) + " seconds left of cooking" 
    #     outside = False
    #     toaster.enable_inside()
    # else:
    #   if(tmp != previous and (tmp - previous) % 5 == 0):
    #     previous = tmp
    #     print "[1] " + str(int(end_time - diff)) + " seconds left of cooking"
    #     outside = True
    #     toaster.enable_outside()
    diff = time.time() - start_time
  print "[1] Releasing the toaster"
  release_toaster()
  print "[1] Toaster released"

def main(argv):
	time = 0
	wait = 0
	try:
		opts, args = getopt.getopt(argv, "")
	except getopt.GetoptError:
		sys.exit(2)
	if len(args) < 1:
		sys.exit(2)

	time = args[0]
	if(len(args) > 1):
		wait = args[1]

	if(wait > 0):
		wait_start(wait, lambda: toast(time))
	else:
		toast(time)

if __name__ == "__main__":
	main(sys.argv[1:])
