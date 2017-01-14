from flask import Flask
from flask_ask import Ask, statement, convert_errors
from motor import Motor
from toaster import Toaster
import RPi.GPIO as GPIO
import logging
import datetime
import time

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

motor = Motor(0, 1, 2, 3) # TODO change these values to the actual pins and duty cycle
toaster = Toaster(0, 1, 2, 3) # TODO change these values to the actual pins

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# wait_start from answer from http://stackoverflow.com/questions/6579127/delay-a-task-until-certain-time
def wait_start(runTime, action):
    startTime = time(*(map(int, runTime.split(':'))))
    while startTime > datetime.today().time(): # you can add here any additional variable to break loop if necessary
        sleep(1)# you can change 1 sec interval to any other
    return action

def make_localtime(tstr):
    """Convert HH:MM in UTC to HH:MM in local timezone."""
    # hours west of UTC
    offset_h = time.timezone // 3600 # hours west of UTC
    # subtract offset, reduce mod24, cast to str
    local_h = str((int(tstr[:2]) - offset_h + 24) % 24)
    # get minutes
    local_m = tstr[3:]
    return "{}:{}".format(local_h, local_m)

@ask.intent('MakeMyToastIntent', mapping={'shade': 'shade', 'time': 'time', 'food': 'food', 'time_identifier': 'time_identifier'})
def make_toast(shade, time, food, time_identifier):

    # if(pinNum != -1):
    #     GPIO.setup(pinNum, GPIO.OUT)
    #     GPIO.output(pinNum, GPIO.HIGH)
    #     if(time != None):
    #         return statement('I will make your {} {} at  {}'.format(food, shade, time))
    #     else:
    #         return statement('I will make your {} {} right now'.format(food, shade))
    # else:
    #     return statement('I think your shade of {} is not correct').format(food)

    # new implementation for this function below this point

    if(time_identifier == "in"):
        time = make_localtime(time)

    if(shade == None):
        shade = "medium"

    if(time != None):
        # will need to open another process using POpen here to handle the waiting and still send message to alexa
        # wait_start(time, lambda: toast(shade, food))
        return statement('I will make your {} {} at  {}'.format(food, shade, time))
    else:
        # toast(shade, food)
        return statement('I will make your {} {} right now'.format(food, shade, time))

def toast(shade, food):
    engage_toaster()
    wait_time = 0
    if(food == "toast"):
        # turn off bagel mode
        if(shade == "light"):
            wait_time = 1 # TODO fix value
        elif(shade == "medium"):
            wait_time = 1 # TODO fix value
        elif(shade == "dark"):
            wait_time = 1 # TODO fix value
        else:
            wait_time = 0
    elif(food == "bagel"):
        # turn on bagel mode
        if(shade == "light"):
            wait_time = 1 # TODO fix value
        elif(shade == "medium"):
            wait_time = 1 # TODO fix value
        elif(shade == "dark"):
            wait_time = 1 # TODO fix value
        else:
            wait_time = 0
    else:
        wait_time = 0
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
    release_toaster()

def engage_toaster():
    motor.clockwise()
    while(!toaster.is_toaster_on()):
        pass
    toaster.enable_solenoid()
    motor.stop()
    toaster.enable_heater()

def release_toaster():
    toaster.disable_heater()
    motor.counterclockwise()
    sleep(2)
    motor.stop()
    toaster.disable_solenoid()

if __name__ == "__main__":
    app.run()
