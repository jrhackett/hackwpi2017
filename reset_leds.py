import RPi.GPIO as GPIO

pins = [2, 4, 26]

GPIO.setmode(GPIO.BCM)

def main():
    for i in pins:
        GPIO.setup(i, GPIO.OUT)
        GPIO.output(i, GPIO.LOW)

if __name__ == "__main__":
    main()
