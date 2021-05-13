import RPi.GPIO as GPIO
from time import sleep
IR1 = 31
IR2 =33
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)
while(1):
    sensor1 = GPIO.input(IR1)
    sensor2 = GPIO.input(IR2)
    if sensor1 and sensor2 == 1:
        print("GO to 1 or 2 ")
    elif sensor1 == 0 and sensor2 == 1:
        print("GO to 2")
    elif sensor1 == 1 and sensor2 == 0:
        print("GO to 1")
    elif sensor1 == 0 and sensor2 == 0:
        print("PARKING FULL")
    else:
        print("Unavailable")
        
GPIO.cleanup()
