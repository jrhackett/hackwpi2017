from flask import Flask
from flask_ask import Ask, statement, convert_errors
from motor import Motor
import RPi.GPIO as GPIO
import logging
from datetime import datetime, time
from time import sleep


# example code for waiting till certain time from http://stackoverflow.com/questions/6579127/delay-a-task-until-certain-time
# def act(x):
#     return x+10

# def wait_start(runTime, action):
#     startTime = time(*(map(int, runTime.split(':'))))
#     while startTime > datetime.today().time(): # you can add here any additional variable to break loop if necessary
#         sleep(1)# you can change 1 sec interval to any other
# return action

# wait_start('15:20', lambda: act(100))



GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

motor = Motor(0, 1, 2, 3) # TODO change these values to the actual pins and duty cycle

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('MakeMyToastIntent', mapping={'shade': 'shade', 'time': 'time', 'food': 'food'})
def make_toast(shade, time, food):
    # if(shade != None):
    #     pinNum = -1
    #     if(shade == "light"):
    #         pinNum = 2
    #     elif (shade == "medium"):
    #         pinNum = 4
    #     elif (shade == "dark"):
    #         pinNum = 26
    # else:
    #     pinNum = 4
    #     shade = "medium"

    # # handle time eventually

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
    if(time != None):
        # might have to convert time here
        print time
        return statement('I will make your {} {} at  {}'.format(food, shade, time))
        # wait_start(time, lambda: toast(shade, food))
    else:
        # toast(shade, food)
        print "toasting"
        return statement('I will make your {} {} at  {}'.format(food, shade, time))




def toast(shade, food):
    engage_toaster()
    if(food == "toast"):
        # turn off bagel mode
        if(shade == "light"):
            # wait time for light toast
        elif(shade == "medium"):
            # wait time for medium toast
        elif(shade == "dark"):
            # wait time for dark toast
        else:
            # default
    elif(food == "bagel"):
        # turn on bagel mode
        if(shade == "light"):
            # wait time for light bagel
        elif(shade == "medium"):
            # wait time for medium bagel
        elif(shade == "dark"):
            # wait time for dark bagel
        else:
            # default
    else:
        # default

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
