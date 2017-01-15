from flask import Flask
from flask_ask import Ask, statement, convert_errors
from motor import Motor
from toaster import Toaster
import RPi.GPIO as GPIO
import logging
import datetime
import time
from subprocess import Popen

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

motor = Motor(13, 19, 6, 100)
toaster = Toaster(25, 8, 24, 7)

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# TODO fix values for these wait times
# should be in whole seconds
wait_time_lookup = { \
    'toast': {'light': 10, 'medium': 22, 'dark': 30}, \
    'bagel': {'light': 10, 'medium': 20, 'dark': 30} \
}

def construct_time_break(time):
    t = int(time)
    to_return = ""
    while(t > 10):
        to_return += '<break time="10s"/> '
        t -= 10
    if(t > 0):
        to_return += '<break time="' + str(t) + 's"/>'
    return to_return

@ask.intent('MakeMyToastIntent', mapping={'shade': 'shade', 'time': 'time', 'food': 'food', 'time_identifier': 'time_identifier'})
def make_toast(shade, time, food, time_identifier):

    # only needed for testing due to time zone issues
    # if(time_identifier == "in"):
    #     time = make_localtime(time)

    if(shade == None):
        shade = 'medium'

    if(time != None):
        subprocess.Popen('./sub.sh ' + str(wait_time_lookup[food][shade]) + ' ' + time)
        return statement('I will make your {} {} at  {}'.format(food, shade, time))
    else:
        subprocess.Popen('./sub.sh ' + str(wait_time_lookup[food][shade]))
        return statement('<speak>I will make your ' + str(food) + ' ' + str(shade) + ' right now. ' + construct_time_break(wait_time_lookup[food][shade]) +' Your toast is done.</speak>')

if __name__ == "__main__":
    app.run()
