import RPi.GPIO as GPIO 
from functions import servoOpenClose
import time
GPIO.setmode(GPIO.BOARD)
servoPin =11
GPIO.setup(servoPin,GPIO.OUT)

result = int(input("where to"))
if result == 1:
    servoOpenClose