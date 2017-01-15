from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging
import datetime
import time
from subprocess import Popen

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# TODO fix values for these wait times
# should be in whole seconds
wait_time_lookup = { \
    'toast': {'light': 100, 'medium': 150, 'dark': 200}, \
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

    if(shade == None):
        shade = 'medium'

    if(time != None):
        Popen('./sub.sh ' + str(wait_time_lookup[food][shade]) + ' ' + time, shell=True, executable="/bin/bash")
        # TODO fix this for SSML
        return statement('I will make your {} {} at  {}'.format(food, shade, time))
    else:
        Popen('./sub.sh ' + str(wait_time_lookup[food][shade]), shell=True, executable="/bin/bash")
        return statement('<speak>I will make your ' + str(food) + ' ' + str(shade) + ' right now. ' + construct_time_break(wait_time_lookup[food][shade] + 7) +' Your toast is done.</speak>')

if __name__ == "__main__":
    app.run()
