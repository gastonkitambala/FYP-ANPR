import cv2
from functions import checkEmptySlot, sendEmail #servoOpenClose, 
from functions import checkEmptySlot
from sendmsdbig import sender
import drivers
display = drivers.Lcd()
from PlateExtraction import extraction
from OpticalCharacterRecognition import ocr
from OpticalCharacterRecognition import check_if_string_in_file
import RPi.GPIO as GPIO
import time 
GPIO.setmode(GPIO.BOARD)
servoPin =11
exitIR = 37
GPIO.setup(exitIR, GPIO.IN)
GPIO.setup(servoPin,GPIO.OUT)
pwm = GPIO.PWM(servoPin, 50)
exitSensor = GPIO.input(exitIR) 

#ALPR
    
image = cv2.imread('./CarPictures/001.jpg')
plate = extraction(image)
#cv2.imshow('frame',plate)
text = ocr(plate)
text = ''.join(e for e in text if e.isalnum())
print(text, end = " ")
content = str(text)
if check_if_string_in_file('./Database/Database.txt', text) and text != "":
    print('Registered')
    display.lcd_display_string("WELCOME:", 1)
    display.lcd_display_string(text, 2)
    time.sleep(2)
    #IR(Empty Slot)
    checkEmptySlot()
    time.sleep(1)
    #ServoMotor
    #servoOpenClose()
    pwm.start(2)
    time.sleep(.5)
    pwm.ChangeDutyCycle(7)
    time.sleep(10)
    pwm.ChangeDutyCycle(2)
    time.sleep(1)
    pwm.stop()
    ##### end servo
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
    
else:
    print("Not Registered")
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
    time.sleep(1)
    time.sleep(3)
    display.lcd_clear()
#exit Section
if exitSensor == 0:
    #ServoMotor
    #servoOpenClose()
    pwm.start(2)
    time.sleep(.5)
    pwm.ChangeDutyCycle(7)
    time.sleep(10)
    pwm.ChangeDutyCycle(2)
    time.sleep(1)
    pwm.stop()
    #eND SERVO


