from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('MakeMyToastIntent', mapping={'shade': 'shade', 'time': 'time'})
def make_toast(shade, time):
    pinNum = -1
    if(shade == "light"):
        pinNum = 2
    elif (shade == "medium"):
        pinNum = 4
    elif (shade == "dark"):
        pinNum = 26
    if(pinNum != -1):
        GPIO.setup(pinNum, GPIO.OUT)
        GPIO.output(pinNum, GPIO.HIGH)
        return statement('I will make your toast {} at  {}'.format(shade, time))
    else:
        return statement('I think your shade of toast is not correct')

if __name__ == "__main__":
    app.run()
