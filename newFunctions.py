import RPi.GPIO as GPIO
import time
#Email Server
import smtplib
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login("gastonkitambala@gmail.com", "kitambalas1998")
####
import drivers
display = drivers.Lcd()

servoPin =11
IR1 = 31
IR2 = 33
exitIR = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)
GPIO.setup(exitIR, GPIO.IN)
GPIO.setup(servoPin,GPIO.OUT)
#pwm = GPIO.PWM(servoPin, 50)

def servoOpenClose():
    pwm.start(2)
    time.sleep(.5)
    pwm.ChangeDutyCycle(7)
    time.sleep(10)
    pwm.ChangeDutyCycle(2)
    time.sleep(10)
    pwm.stop()

def slotsAvailable():
    if sensor1 or sensor2 == 0:
         availableSlots =1
    if sensor1 ==1 and sensor2 ==1:
        availableSlots = 2
    if sensor1 == 0 and sensor2 == 0:
        availableSlots = 0


def checkEmptySlot():
    sensor1 = GPIO.input(IR1)
    sensor2 = GPIO.input(IR2)
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
        
def sendEmail(text):
    #currentTime = time.ctime()
    emailContent = ("Vehicle: " + text + "Has been granted access at: " )
    server.sendmail("gastonkitambala@gmail.com","gastonkitambala@yahoo.com",emailContent)

def allowCar() :
    print('Registered')
    display.lcd_display_string("WELCOME:", 1)
    display.lcd_display_string(text, 2)
    time.sleep(2)
    #IR(Empty Slot)
    checkEmptySlot()
    time.sleep(1)
    #ServoMotor
    servoOpenClose()
    #send email
    sendTo = 'gastonkitambala@yahoo.com'
    emailSubject = "APPROACHING VEHICLE!"
    emailContent = "The vehicle with license number: " + content +" "+"has been granted access on:\n " + time.ctime()
    #sender.sendmail(sendTo, emailSubject, emailContent)
    print("Email Sent")
    time.sleep(1)
    GPIO.cleanup()
    time.sleep(1)
    display.lcd_clear()


def unauthorised(text, content) :
    print('Not Registered')
    display.lcd_display_string(text, 1)
    display.lcd_display_string("NOT REGISTERED", 2)
    time.sleep(3)
    display.lcd_display_string("ACCESS DENIED   ", 2)
    time.sleep(4)
    display.lcd_display_string("Call Admin      ", 2)
    sendTo = 'gastonkitambala@yahoo.com'
    emailSubject = "ACCESS DENIED!"
    emailContent = "The vehicle with license number: " + content +" "+"has been denied access on:\n " + time.ctime()
    #sender.sendmail(sendTo, emailSubject, emailContent)
    print("Email Sent")
    time.sleep(3)
    display.lcd_clear()

