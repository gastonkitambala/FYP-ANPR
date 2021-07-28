#FUnctions Used for the Optical Opto_Gate System
import RPi.GPIO as GPIO #Gpio Library
import time
#Importing Email Server
import smtplib  #Email Library
server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls() #Start the server for email
server.login("gastonkitambala@gmail.com", "kitambalas1998")
####  LCD Drivers
import drivers
display = drivers.Lcd()

#GPIO Setup
servoPin = 11 #Pin 11 for Servo Motor
#Infrared sensor for partin 1,2 and exit
IR1 = 31   
IR2 = 33
exitIR = 37
GPIO.setmode(GPIO.BOARD) #Gpio.Board setmode used
#IR1, IR2 And exitIR set as inputs
GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)
GPIO.setup(exitIR, GPIO.IN)
GPIO.setup(servoPin,GPIO.OUT)
pwm = GPIO.PWM(servoPin, 50) #Starting Pulse width Modulation at 50Hz for Servo Motor
#Listening to Sensor 1 and Sensor 2 for input 
sensor1 = GPIO.input(IR1)
sensor2 = GPIO.input(IR2)

#Function for Opening and Closing the ServoMotor for after access Granting
def servoOpenClose():
    pwm.start(2)
    time.sleep(.5)
    pwm.ChangeDutyCycle(7)
    time.sleep(10)
    pwm.ChangeDutyCycle(2)
    time.sleep(10)
    pwm.stop()

#Function to check the available parking space
def slotsAvailable():
    if sensor1 or sensor2 == 0:
         availableSlots = 1
    if sensor1 ==1 and sensor2 ==1:
        availableSlots = 2
    if sensor1 == 0 and sensor2 == 0:
        availableSlots = 0


def checkEmptySlot():
    exitSensor = GPIO.input(exitIR)
    
    if sensor1 == 1 and sensor2 == 1:
        display.lcd_display_string("L1:OPEN-L2:OPEN", 2)
        #print("GO to 1 or 2 ")
    elif sensor1 == 0 and sensor2 == 1:
        display.lcd_display_string("Slot2: OPEN", 2)
        #print("GO to 2")
    elif sensor1 == 1 and sensor2 == 0:
        display.lcd_display_string("Slot1: OPEN", 2)
        #print("GO to 1")
    elif sensor1 == 0 and sensor2 == 0:
        display.lcd_display_string("PARKING FULL", 2)
        #print("PARKING FULL")
    else:
        print("Unavailable")
        
#Function for sending Email
def sendEmail(text):
    #currentTime = time.ctime()
    emailContent = ("Vehicle: " + text + "Has been granted access at: " )
    server.sendmail("gastonkitambala@gmail.com","gastonkitambala@yahoo.com",emailContent)

