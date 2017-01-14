from flask import Flask
from flask_ask import Ask, statement, convert_errors
from motor import Motor
import RPi.GPIO as GPIO
import logging
import datetime
import time

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

motor = Motor(0, 1, 2, 3) # TODO change these values to the actual pins and duty cycle

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

    if(time != None):
        # might have to convert time here
        times = time.split(":")
        t = datetime.time(int(times[0].encode("utf-8")), int(times[1].encode("utf-8")))
        return statement('I will make your {} {} at  {}'.format(food, shade, time))
        # wait_start(time, lambda: toast(shade, food))
    else:
        # toast(shade, food)
        return statement('I will make your {} {} at  {}'.format(food, shade, time))

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
    release_toaster()

def engage_toaster():
    motor.clockwise()
    sleep(2)
    # engage toaster solenoid
    motor.stop()

def release_toaster():
    motor.counterclockwise()
    sleep(2)
    # release toaster solenoid
    motor.stop()

if __name__ == "__main__":
    app.run()
