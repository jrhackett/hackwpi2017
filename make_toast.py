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

motor = Motor(13, 19, 6, 100)
toaster = Toaster(25, 8, 24, 7)

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# TODO fix values for these wait times
# should be in whole seconds
wait_time_lookup = { \
    'toast': {'light': 10, 'medium': 10, 'dark': 30}, \
    'bagel': {'light': 10, 'medium': 20, 'dark': 30} \
}

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

def construct_time_break(time):
    t = int(time)
    to_return = ''
    while(t > 10):
        to_return += '<break time="10s" /> '
        t -= 10
    if(t > 0):
        to_return += '<break time=' + str(t) + '" />'
    return to_return

@ask.intent('MakeMyToastIntent', mapping={'shade': 'shade', 'time': 'time', 'food': 'food', 'time_identifier': 'time_identifier'})
def make_toast(shade, time, food, time_identifier):

    # only needed for testing due to time zone issues
    # if(time_identifier == "in"):
    #     time = make_localtime(time)

    if(shade == None):
        shade = 'medium'

    if(time != None):
        # will need to open another process using POpen here to handle the waiting and still send message to alexa
        # wait_start(time, lambda: toast(shade, food))
        # return statement('I will make your {} {} at  {}'.format(food, shade, time))
        return statement('You done fucked up bro')
    else:
        # toast(shade, food)
        # return statement('I will make <break time="2s"/> your {} {} right now'.format(food, shade, time))
        return statement('<speak>I will make your ' + str(food) + ' ' + str(shade) + ' right now. ' + construct_time_break(wait_time_lookup[food][shade]) +' Your toast is done.</speak>')
def toast(shade, food):
    engage_toaster()
    wait_time = 0
    wait_time = wait_time_lookup[food][shade]
    start_time = time.time()
    diff = time.time() - start_time
    outside = False
    while(diff < wait_time):
        if(diff % 5 == 0):
            if(outside):
                outside = False
                toaster.enable_inside()
            else:
                outside = True
                toaster.enable_outside()
        diff = time.time() - start_time
    release_toaster()

def engage_toaster():
    motor.clockwise()
    while(not toaster.is_toaster_on()):
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
