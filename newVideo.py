#Importin functios from the function file
import cv2
#from functions import *
from functions import checkEmptySlot, sendEmail
from functions import checkEmptySlot
from sendmsdbig import sender
import drivers
from PlateExtraction import extraction
from OpticalCharacterRecognition import ocr
from OpticalCharacterRecognition import check_if_string_in_file
import RPi.GPIO as GPIO
import time 

#GPIO Setup
GPIO.setmode(GPIO.BOARD)
servoPin =11
IR1 = 31
IR2 = 33
exitIR = 37
GPIO.setup(exitIR, GPIO.IN)
PIO.setup(IR1, GPIO.IN)
GPIO.setup(IR2, GPIO.IN)
GPIO.setup(servoPin,GPIO.OUT)
sensor1 = GPIO.input(IR1)
sensor2 = GPIO.input(IR2)
exitSensor = GPIO.input(exitIR)

display = drivers.Lcd()
pwm = GPIO.PWM(servoPin, 50) #PWM initialised at 50Hz frequency
availableSlots = 0
#email
sendTo = 'gastonkitambala@yahoo.com'
emailSubject = "APPROACHING VEHICLE!"
emailContent = "The vehicle with license number: " + content +" "+"has been granted access on:\n " + time.ctime()

#beginning of OpenCv for License Plate recognition
cap = cv2.VideoCapture(0)
while(True):
    ret,frame = cap.read()
    plate = extraction(frame)
    try:
        text = ocr(plate)
        text = ''.join(e for e in text if e.isalnum())
    except:
        continue
        
    if text != '':
        print(text,end=" ")
        content = str(text)
        while len(content) >= 5: #if the length of number plate is more than 5 letters
            if check_if_string_in_file('./Database/Database.txt', text):
                print('Registered')
                display.lcd_display_string("WELCOME:", 1)
                display.lcd_display_string(text, 2)
                time.sleep(2)
                if sensor1 == 1 and sensor2 == 1:
                    availableSlots = 2
                    print("The Available Slots are :", availableSlots)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string(availableSlots, 2)
                    time.sleep(3)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string("1:OPEN - 2:OPEN", 2)
                    servoOpenClose()
                    sender.sendmail(sendTo, emailSubject, emailContent)
                    print("Email Sent")
                    time.sleep(3)
                    slotsAvailable()

                elif sensor1 == 0 and sensor2 == 1:
                    availableSlots = 1
                    print("The Available Slots are :", availableSlots)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string(availableSlots, 2)
                    time.sleep(3)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string("1:USED - 2:OPEN", 2)
                    servoOpenClose()
                    sender.sendmail(sendTo, emailSubject, emailContent)
                    print("Email Sent")
                    time.sleep(3)
                    slotsAvailable()
                elif sensor1 == 1 and sensor2 == 0:
                    availableSlots = 1
                    print("The Available Slots are :", availableSlots)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string(availableSlots, 2)
                    time.sleep(3)
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string("1:OPEN - 2:USED", 2)
                    servoOpenClose()
                    sender.sendmail(sendTo, emailSubject, emailContent)
                    print("Email Sent")
                    time.sleep(3)
                    slotsAvailable()
                elif sensor1 == 0 and sensor2 == 0:
                    availableSlots = 0
                    print("No Parking Slot available")
                    display.lcd_display_string("PARKING FULL", 1)
                    display.lcd_display_string("No Parking", 2)
                    time.sleep(3)
                    slotsAvailable()
                    #print("PARKING FULL")
                else:
                    display.lcd_display_string("Issue Found..", 1)
                    display.lcd_display_string("Retrying...", 2)
                    time.sleep(3)
                    print("Retrying......")

                time.sleep(1)
                GPIO.cleanup()
                time.sleep(1)
                display.lcd_clear()
            else:
                print('Not Registered')
                time.sleep(3)
                print(availableSlots)
                display.lcd_display_string(text, 1)
                display.lcd_display_string("NOT REGISTERED", 2)
                time.sleep(3)
                display.lcd_display_string("ACCESS DENIED   ", 2)
                time.sleep(4)
                display.lcd_display_string("Call Admin      ", 2)
                time.sleep(4)
                sendTo = 'gastonkitambala@yahoo.com'
                emailSubject = "ACCESS DENIED!"
                emailContent = "The vehicle with license number: " + content +" "+"has been denied access on:\n " + time.ctime()
                sender.sendmail(sendTo, emailSubject, emailContent)
                print("Email Sent")
                time.sleep(3)
                display.lcd_clear()

            #Exit 
            if exitSensor == 0:
                if sensor1 or sensor2 == 0:
                    availableSlots = 1
                    servoOpenClose()
                    availableSlots -=1
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string(availableSlots, 2)
                if sensor1 ==1 and sensor2 ==1:
                    availableSlots = 2
                    continue
                if sensor1 == 0 and sensor2 == 0:
                    availableSlots = 0
                    servoOpenClose()
                    availableSlots -=1
                    display.lcd_display_string("AVAILABLE LOTS: ", 1)
                    display.lcd_display_string(availableSlots, 2)

        #else:
         #   print("Retrying.....")
        
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
#exit Section
#if exitSensor == 0:
    #ServoMotor
    #servoOpenClose()
    #pwm.start(2)
    #time.sleep(.5)
    #pwm.ChangeDutyCycle(7)
    #time.sleep(10)
    #pwm.ChangeDutyCycle(2)
    #time.sleep(1)
    #pwm.stop()
    #eND SERVO
    


